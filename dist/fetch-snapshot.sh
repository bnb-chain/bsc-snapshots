#!/bin/bash
#set -v
set -e

handle_interrupt() {
    echo "Exiting script..."
    exit 1
}
trap handle_interrupt SIGINT

# Detect the number of leading path components to strip before "geth/".
# e.g. "server/data-seed/geth/chaindata/..." -> strip 2 ("server/data-seed/")
detect_strip_components() {
    local archive="$1"
    local match
    match=$(tar -I lz4 -tf "$archive" 2>/dev/null | grep -m1 'geth/' || true)
    if [[ -z "$match" ]]; then
        echo 0
        return
    fi
    local prefix="${match%%geth/*}"
    echo "$prefix" | tr -cd '/' | wc -c | tr -d ' '
}

show_help() {
    echo "Usage: $0 [options] <CSV_FILE>"
    echo "Options:"
    echo "  -p, --prune-ancient    Skip files containing '-blocks-', and will support later"
    echo "  -d, --download        Download files from CSV"
    echo "  -e, --extract         Extract downloaded archives from CSV"
    echo "  -c, --checksum        Verify MD5 checksums"
    echo "  -C, --clean           Delete all files listed in the CSV"
    echo "  -D, --download-dir <dir>  Set the download directory (default: .)"
    echo "  -E, --extract-dir <dir>   Set the extract directory (default: same as download dir)"
    echo "  -a, --auto-delete         Whether to auto delete downloaded file after uncompress"
    echo "  -h, --help            Show this help message"
}

PRUNE_ANCIENT=false
DOWNLOAD=false
EXTRACT=false
CHECKSUM=false
CLEAN=false
DOWNLOAD_DIR="./"
EXTRACT_DIR="$DOWNLOAD_DIR"
AUTO_DELETE=false

# parse command line
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--prune-ancient)
        PRUNE_ANCIENT=true
        shift
        ;;
        -d|--download)
        DOWNLOAD=true
        shift
        ;;
        -e|--extract)
        EXTRACT=true
        shift
        ;;
        -c|--checksum)
        CHECKSUM=true
        shift
        ;;
        -C|--clean)
        CLEAN=true
        shift
        ;;
        -a|--auto-delete)
        AUTO_DELETE=true
        shift
        ;;
        -D|--download-dir)
        if [ "$DOWNLOAD_DIR" == "$EXTRACT_DIR" ]; then
          DOWNLOAD_DIR="$2"
          EXTRACT_DIR="$2"
        else
          DOWNLOAD_DIR="$2"
        fi
        shift
        shift
        ;;
        -E|--extract-dir)
        EXTRACT_DIR="$2"
        shift
        shift
        ;;
        -h|--help)
        show_help
        exit 0
        ;;
        *)
        CSV_FILE="$1"
        shift
        ;;
    esac
done

#echo $PRUNE_ANCIENT $DOWNLOAD $EXTRACT $CHECKSUM $CLEAN $AUTO_DELETE $DOWNLOAD_DIR $EXTRACT_DIR

if [[ -z "$CSV_FILE" ]]; then
    echo "Error: CSV file is required."
    show_help
    exit 1
fi

if [[ ! "$CSV_FILE" =~ \.csv$ ]] && [[ "$PRUNE_ANCIENT" = true ]]; then
    CSV_FILE=$CSV_FILE-pruneancient
fi
if [[ ! -f "$CSV_FILE" ]]; then
    if [[ ! -f "$CSV_FILE.csv" ]]; then
        remote_file=https://raw.githubusercontent.com/bnb-chain/bsc-snapshots/main/dist/$CSV_FILE.csv
        echo "try to download $CSV_FILE.csv from $remote_file"
        wget -O $CSV_FILE.csv $remote_file
    fi
    CSV_FILE=$CSV_FILE.csv
fi

mkdir -p "$DOWNLOAD_DIR"
mkdir -p "$EXTRACT_DIR"

if [[ "$DOWNLOAD" = true ]]; then
    echo "download file into $DOWNLOAD_DIR ..."
    while IFS=',' read -r filename url md5 size; do
        # skip the title roe
        [[ "$filename" == "filename" ]] && continue

        download_path="$DOWNLOAD_DIR/$filename"
        downloaded=false
        # check if the file has been downloaded
        if [[ -f "$download_path" ]] && [[ ! -f "$download_path.aria2" ]]; then
            if [[ "$CHECKSUM" = true ]]; then
              echo "$md5 $download_path" | md5sum -c --quiet
              if [[ $? -eq 0 ]]; then
                  echo "Skipping $filename - already downloaded and verified"
                  downloaded=true
              else
                  echo "Deleting $filename - MD5 mismatch or file corrupted"
                  rm -f "$download_path"
              fi
            else
              echo "Skipping $filename - already downloaded"
              downloaded=true
            fi
        fi

        if [[ "$downloaded" = false ]]; then
          echo "Downloading $filename from $url"
          aria2c -s14 -x14 -k100M --continue --dir="$DOWNLOAD_DIR" "$url"

          if [[ $? -eq 0 ]]; then
              if [[ "$CHECKSUM" = true ]]; then
                echo "$md5 $download_path" | md5sum -c --quiet
                if [[ $? -eq 0 ]]; then
                    echo "Download and verification complete: $filename"
                else
                    echo "Download complete, but MD5 verification failed: $filename"
                    exit 1
                fi
              else
                echo "Download complete: $filename"
              fi
          else
              echo "Error downloading $filename"
          fi
        fi

        # if enable auto delete, just uncompress the file and delete
        if [[ "$EXTRACT" = true && "$AUTO_DELETE" = true ]]; then
          strip=$(detect_strip_components "$download_path")
          echo "Extracting $filename (strip-components=$strip)"
          tar -I lz4 -xvf "$download_path" -C "$EXTRACT_DIR" --strip-components="$strip"
          if [[ $? -eq 0 ]]; then
              rm -f "$download_path"
              echo "Extraction complete and removed: $filename"
          else
              echo "Error extracting $filename"
              exit 1
          fi
        fi
    done < "$CSV_FILE"
fi

if [[ "$EXTRACT" = true && "$AUTO_DELETE" = false ]]; then
    echo "extract file into $EXTRACT_DIR..."
    while IFS=',' read -r filename url md5 size; do
        # skip the title row
        [[ "$filename" == "filename" ]] && continue

        download_path="$DOWNLOAD_DIR/$filename"
        extract_path="$EXTRACT_DIR/$filename"

        if [[ ! -f "$download_path" ]]; then
            echo "Error: $filename not found, skipping extraction"
            exit 1
        fi

        if [[ "$CHECKSUM" = true && "$DOWNLOAD" = false ]]; then
          echo "$md5 $download_path" | md5sum -c --quiet
          if [[ $? -eq 0 ]]; then
            echo "$filename - already downloaded and verified"
          else
            echo "Download complete, but MD5 verification failed: $filename"
            exit 1
          fi
        fi

        strip=$(detect_strip_components "$download_path")
        echo "Extracting $filename (strip-components=$strip)"
        tar -I lz4 -xvf "$download_path" -C "$EXTRACT_DIR" --strip-components="$strip"

        if [[ $? -eq 0 ]]; then
            echo "Extraction complete: $filename"
        else
            echo "Error extracting $filename"
            exit 1
        fi
    done < "$CSV_FILE"
fi

if [[ "$CLEAN" = true ]]; then
    while IFS=',' read -r filename url md5 size; do
        [[ "$filename" == "filename" ]] && continue

        download_path="$DOWNLOAD_DIR/$filename"
        extract_path="$EXTRACT_DIR/$filename"

        if [[ -f "$download_path" ]]; then
            echo "Deleting $filename"
            rm -f "$download_path"
        fi
    done < "$CSV_FILE"
fi