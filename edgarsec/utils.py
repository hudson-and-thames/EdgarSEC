from tqdm import tqdm
from requests import Response
from pathlib import Path
import zipfile


def _download_with_progress(response: Response, file_path: Path) -> None:
    total_size = int(response.headers.get('content-length', 0))

    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'wb') as file:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading File', initial=0) as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                if not chunk:
                    continue
                file.write(chunk)
                pbar.update(len(chunk))


def _unzip_file(file_path: Path, extract_to: str | Path) -> None:

    extract_to = Path(extract_to)

    if zipfile.is_zipfile(file_path):
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        except (OSError, zipfile.BadZipFile) as err:
            raise ValueError(f"Unzip failed with error: {err}")
    else:
        raise ValueError(f"{file_path} is not a zip file")