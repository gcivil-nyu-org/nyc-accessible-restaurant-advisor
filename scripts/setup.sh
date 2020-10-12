RED='\033[0;31m'          # Red
GREEN='\033[0;32m'        # Green
COLOR_OFF='\033[0m'       # Text Reset

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$SCRIPT_DIR/.."

if [[ -z $VIRTUAL_ENV ]]; then
  echo "$RED""You haven't activated virtualenv."
  echo "Try the following command to activate your virtualenv:"
  echo "  python3 -m venv your_virtualenv_name"
  echo "  source your_virtualenv_name/bin/activate"
  echo "Exit...""$COLOR_OFF"
  exit 0 ;
else
  echo "$GREEN""virtualenv activated""$COLOR_OFF"
fi

echo ""
echo "$GREEN""Running pip install -r requirements.txt...""$COLOR_OFF"
pip install -r requirements.txt || exit 1
echo "$GREEN""[Success] pip install -r requirements.txt""$COLOR_OFF"
