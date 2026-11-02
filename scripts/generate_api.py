"""Refresh the public API metadata from the local Pixel Legion Maker project.

Compiles the product's Runtime and Editor assemblies with the references and defines Unity used
(read from Unity's own compiler response files under Library/Bee), runs `docfx metadata` on the
result and keeps only sanitized declaration YAML. Source files, source links, assemblies and the
temporary build stay under .work/ and are never published.
Run it from a project that the Unity Editor has already compiled.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from xml.sax.saxutils import escape

import yaml


SITE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT = SITE_ROOT.parents[1]
DOCFX_VERSION = "2.81.0"
ASSEMBLIES = ["PixelUnitStudio.Runtime", "PixelUnitStudio.Editor"]
EXCLUDED_SOURCES = ("Assets/PixelUnitStudio/Editor/Release/",)  # development tools, not in the package
SOURCE_FIELDS = {"source", "sourceLink", "sourceUrl", "sourceURL", "documentation", "remote", "git"}
ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]|file://|/(?:Users|home|workspace|workspace_ai|tmp|private/var)/")


class DocfxLoader(getattr(yaml, "CSafeLoader", yaml.SafeLoader)):
    """DocFX can emit unquoted '=' scalars, which PyYAML tags as YAML values."""


DocfxLoader.add_constructor("tag:yaml.org,2002:value", lambda loader, node: loader.construct_scalar(node))


def run(command: list[str | Path], cwd: Path) -> None:
    subprocess.run([str(arg) for arg in command], cwd=cwd, check=True)


def clean_metadata(value):
    if isinstance(value, dict):
        return {key: clean_metadata(item) for key, item in value.items() if key not in SOURCE_FIELDS}
    if isinstance(value, list):
        return [clean_metadata(item) for item in value]
    return value


def validate_public_metadata(value, location: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in SOURCE_FIELDS:
                raise ValueError(f"Source metadata remains in {location}: {key}")
            validate_public_metadata(item, location)
    elif isinstance(value, list):
        for item in value:
            validate_public_metadata(item, location)
    elif isinstance(value, str) and ABSOLUTE_PATH.search(value):
        raise ValueError(f"An absolute path remains in public metadata: {location}")


def response_file(project: Path, assembly: str) -> tuple[list[str], list[str], list[str]]:
    """References, defines and sources from the newest Unity compiler response file of an assembly."""
    responses = sorted((project / "Library/Bee/artifacts").glob(f"*/{assembly}.rsp"),
                       key=lambda path: path.stat().st_mtime, reverse=True)
    if not responses:
        raise SystemExit(f"No Unity compiler response file for {assembly}; open the project in Unity first.")
    references, defines, sources = [], [], []
    for line in responses[0].read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("-r:"):
            references.append(line[3:].strip('"'))
        elif line.startswith("-define:"):
            defines.append(line[8:])
        elif line.endswith('.cs"'):
            source = line.strip('"')
            if not source.startswith(EXCLUDED_SOURCES):
                sources.append(source)
    # The product's own assemblies are built here, so their XML documentation comes along.
    references = [r for r in references if Path(r).name.split(".ref.")[0].removesuffix(".dll") not in ASSEMBLIES]
    return references, defines, sources


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--docfx", default=shutil.which("docfx") or str(Path.home() / ".dotnet/tools/docfx.exe"))
    parser.add_argument("--output", type=Path, default=SITE_ROOT / "api-metadata")
    args = parser.parse_args()

    project = args.project_root.resolve()
    work = project / ".work/api-generation"
    output = args.output.resolve()
    docfx_version = subprocess.check_output([args.docfx, "--version"], text=True).strip()
    if docfx_version.split("+", 1)[0] != DOCFX_VERSION:
        raise SystemExit(f"DocFX {DOCFX_VERSION} is required; found {docfx_version}.")

    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    all_sources = []
    for index, assembly in enumerate(ASSEMBLIES):
        references, defines, sources = response_file(project, assembly)
        all_sources += sources
        target = work / assembly
        target.mkdir()
        items = "".join(f'<Compile Include="{escape(str(project / s))}" />' for s in sources)
        items += "".join(f'<Reference Include="{escape(r if Path(r).is_absolute() else str(project / r))}" Private="false" />'
                         for r in references)
        items += "".join(f'<ProjectReference Include="../{dep}/{dep}.csproj" />' for dep in ASSEMBLIES[:index])
        (target / f"{assembly}.csproj").write_text(f'''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.1</TargetFramework><LangVersion>9.0</LangVersion><Nullable>disable</Nullable>
    <AssemblyName>{assembly}</AssemblyName><EnableDefaultCompileItems>false</EnableDefaultCompileItems>
    <DisableImplicitFrameworkReferences>true</DisableImplicitFrameworkReferences><NoStdLib>true</NoStdLib>
    <GenerateDocumentationFile>true</GenerateDocumentationFile><DebugType>none</DebugType>
    <NoWarn>1591;0649;0169;0414;1701;1702;1705</NoWarn><DefineConstants>{';'.join(defines)}</DefineConstants>
  </PropertyGroup>
  <ItemGroup>{items}</ItemGroup>
</Project>
''', encoding="utf-8")
    run(["dotnet", "build", work / ASSEMBLIES[-1] / f"{ASSEMBLIES[-1]}.csproj", "-c", "Release", "--nologo"], work)

    binaries = work / "binaries"
    binaries.mkdir()
    for assembly in ASSEMBLIES:
        for suffix in ("dll", "xml"):
            shutil.copy2(work / assembly / f"bin/Release/netstandard2.1/{assembly}.{suffix}", binaries)
    raw = work / "raw-metadata"
    references = sorted({r for a in ASSEMBLIES for r in response_file(project, a)[0]})
    config = {"metadata": [{"src": [{"src": binaries.as_posix(), "files": ["PixelUnitStudio.*.dll"]}],
                            "references": [r if Path(r).is_absolute() else (project / r).as_posix() for r in references],
                            "dest": raw.as_posix(), "disableGitFeatures": True, "includePrivateMembers": False}]}
    (work / "metadata.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    run([args.docfx, "metadata", work / "metadata.json", "--disableGitFeatures"], work)

    # Validate every document before replacing the previous public metadata.
    sanitized, uids = {}, []
    for path in sorted(raw.glob("*.yml")):
        text = path.read_text(encoding="utf-8-sig")
        marker = text.splitlines()[0] + "\n" if text.startswith("###") else ""
        data = clean_metadata(yaml.load(text, Loader=DocfxLoader))
        validate_public_metadata(data, path.name)
        if isinstance(data, dict):
            uids += [item["uid"] for item in data.get("items", []) if "uid" in item]
        sanitized[path.name] = marker + yaml.dump(data, Dumper=getattr(yaml, "CSafeDumper", yaml.SafeDumper),
                                                 sort_keys=False, allow_unicode=True, width=120)
    if not any(uid.startswith("PixelUnitStudio.Editor") for uid in uids):
        raise SystemExit("API extraction did not produce both assemblies.")
    output.mkdir(parents=True, exist_ok=True)
    for stale in output.glob("*.yml"):
        if stale.name not in sanitized:
            stale.unlink()
    for name, text in sanitized.items():
        (output / name).write_text(text, encoding="utf-8", newline="\n")
    source_hash = hashlib.sha256()
    for source in sorted(all_sources):
        source_hash.update(source.encode("utf-8"))
        source_hash.update((project / source).read_bytes())
    manifest = {"product": "Pixel Legion Maker", "docfx_version": DOCFX_VERSION, "assemblies": ASSEMBLIES,
                "visibility": "public and protected API", "source_sha256": source_hash.hexdigest(),
                "source_files_published": False, "source_links_published": False,
                "metadata_files": len(sanitized), "documented_uids": len(uids)}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
