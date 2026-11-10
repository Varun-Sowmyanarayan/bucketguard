cd "$(dirname "$0")"
source venv/bin/activate
python3 bucketguard.py | tee report.txt
echo ""
echo "Report saved to report.txt"