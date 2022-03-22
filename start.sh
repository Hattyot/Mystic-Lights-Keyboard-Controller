#cd "$(dirname "$(realpath "$0")")"
#export DISPLAY=:0
python src/dbusiface.py
echo "Started mystic lights controller with pid: "$!