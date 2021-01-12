if python --version 2>&1 | grep -1 'Python 3\.'
then
python telegramexporter.py
else
python3 telegramexporter.py
fi