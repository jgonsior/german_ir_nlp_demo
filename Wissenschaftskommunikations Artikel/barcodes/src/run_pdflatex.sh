FOLDER_PATH=$1

if [ -z "$FOLDER_PATH" ]; then
  echo "No folder path provided."
  exit 1
fi

for file in "$FOLDER_PATH"/*.tex; do
  pdflatex "$file"
done