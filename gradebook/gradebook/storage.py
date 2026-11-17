import json
import logging
import re
from pathlib import Path


DATA_FILE = Path("data/gradebook.json")
LOG_FILE = Path("logs/app.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
	filename=LOG_FILE,
	level=logging.INFO,
	format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def empty_data():
	return {"students": [], "courses": [], "enrollments": []}


def load_data():
	try:
		with DATA_FILE.open("r", encoding="utf-8") as file:
			data = json.load(file)
	except FileNotFoundError:
		logger.info("Data file not found; starting with an empty gradebook")
		return empty_data()
	except json.JSONDecodeError as error:
		logger.error("Could not read JSON data: %s", error)
		raise ValueError(
			f"{DATA_FILE} is not valid JSON. Run the seed script or fix the file."
		) from error

	for key in ("students", "courses", "enrollments"):
		if not isinstance(data, dict) or not isinstance(data.get(key), list):
			raise ValueError(f"{DATA_FILE} must contain a '{key}' list.")
	logger.info("Loaded gradebook data")
	return data


def save_data(data):
	DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
	try:
		json_text = json.dumps(data, indent=2)
		json_text = re.sub(
			r'("grades": )\[([^\]]*)\]',
			lambda match: match.group(1) + json.dumps(json.loads("[" + match.group(2) + "]")),
			json_text,
		)
		with DATA_FILE.open("w", encoding="utf-8") as file:
			file.write(json_text)
		logger.info("Saved gradebook data")
	except OSError:
		logger.exception("Could not save gradebook data")
		raise
