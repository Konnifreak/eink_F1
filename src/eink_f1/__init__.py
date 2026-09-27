from .main import app

def main() -> None:
	import uvicorn

	uvicorn.run("eink_f1.main:app", host="0.0.0.0", port=8000)