#!/usr/bin/env bash
set -e

DOMAIN="derenpy"
PO_DIR="po"
LOCALE_DIR="derenpy/locales"
POT_FILE="$PO_DIR/$DOMAIN.pot"

# Define the mapping inline to avoid extra config files
MAPPING="[python: **.py]"

cleanup() {
    if [ -n "$TEMP_MAPPING_FILE" ] && [ -f "$TEMP_MAPPING_FILE" ]; then
        rm -f "$TEMP_MAPPING_FILE"
    fi
}

trap cleanup EXIT INT TERM

case "$1" in
    extract)
        echo "🔍 Extracting strings to $POT_FILE..."

        TEMP_MAPPING_FILE=$(mktemp)
        echo "$MAPPING" > "$TEMP_MAPPING_FILE"

        pybabel extract -F "$TEMP_MAPPING_FILE" -o "$POT_FILE" .
        ;;

    init)
        if [ -z "$2" ]; then echo "Usage: $0 init <lang>"; exit 1; fi
        LANG_CODE="$2"
        PO_FILE="$PO_DIR/$LANG_CODE.po"

        if [ -f "$PO_FILE" ]; then
            echo "⚠️  $PO_FILE already exists. Use './$0 update' to merge new strings."
            exit 1
        fi

        echo "🆕 Initializing $LANG_CODE..."
        # Create the flat .po file
        pybabel init -i "$POT_FILE" -o "$PO_FILE" -l "$LANG_CODE"

        # Immediately compile to create the runtime structure
        "$0" compile
        ;;

    update)
        echo "🔄 Updating .po files from $POT_FILE..."
        # Update all .po files in the flat directory
        for po_file in "$PO_DIR"/*.po; do
            if [ -f "$po_file" ]; then
                # Skip the pot file if the glob catches it (unlikely but safe)
                if [[ "$po_file" == *.pot ]]; then continue; fi

                lang=$(basename "$po_file" .po)

                echo "Updating $lang..."
                pybabel update -i "$POT_FILE" -o "$po_file" -l "$lang" "$po_file"
            fi
        done
        # Recompile all to ensure locale/ is in sync
        "$0" compile
        ;;

    compile)
        echo "🔨 Compiling all .po to .mo..."
        rm -rf "$LOCALE_DIR"
        mkdir -p "$LOCALE_DIR"

        for po_file in "$PO_DIR"/*.po; do
            if [ -f "$po_file" ]; then
                lang=$(basename "$po_file" .po)

                # Skip pot files
                if [ "$lang" = "$DOMAIN" ]; then continue; fi

                out_dir="$LOCALE_DIR/$lang/LC_MESSAGES"
                mkdir -p "$out_dir"

                # Compile flat .po to verbose .mo
                pybabel compile -i "$po_file" -o "$out_dir/$DOMAIN.mo"
                echo "  Compiled $lang -> $out_dir/$DOMAIN.mo"
            fi
        done

        if [ "$(ls -A $LOCALE_DIR 2>/dev/null)" = "" ]; then
            echo "⚠️  No .po files found in $PO_DIR to compile."
        else
            echo "✅ Runtime structure ready in $LOCALE_DIR/"
        fi
        ;;

    *)
        echo "Usage: $0 {extract|init <lang>|update|compile}"
        exit 1
        ;;
esac
