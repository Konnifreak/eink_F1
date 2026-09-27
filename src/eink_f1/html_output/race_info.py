import base64
import html
from pathlib import Path
from typing import Any


def _background_data_uri() -> str:
	image_path = Path(__file__).resolve().parents[3] / "img" / "back2.png"
	image_data = base64.b64encode(image_path.read_bytes()).decode("ascii")
	return f"data:image/png;base64,{image_data}"


def _text(value: Any, fallback: str = "") -> str:
	return html.escape(str(value if value is not None else fallback))


def _driver_name(driver: dict[str, Any]) -> str:
	full_name = driver.get("full_name", "Unknown driver")
	name_parts = str(full_name).split(" ", 1)
	return _text(name_parts[1] if len(name_parts) == 2 else full_name)


def _driver_surname(driver: dict[str, Any]) -> str:
	full_name = driver.get("full_name", "Unknown driver")
	name_parts = str(full_name).split(" ", 1)
	return _text(name_parts[0] if name_parts else full_name)


def _driver_card(result: dict[str, Any], place: int) -> str:
	driver = result.get("driver_info") or {}
	team_colour = _text(driver.get("team_colour") or "666666").lstrip("#")
	headshot_url = _text(driver.get("headshot_url") or "")
	image = f'<img src="{headshot_url}" alt="{_driver_name(driver)}">' if headshot_url else ""
	return f"""
		<article class="podium-card place-{place}" style="--team-colour: #{team_colour}">
			<div class="podium-place">{place}</div>
			{image}
			<div class="driver-surname">{_driver_surname(driver)}</div>
			<div class="driver-name">{_driver_name(driver)}</div>
			<div class="team-name">{_text(driver.get("team_name"), "Unknown team")}</div>
		</article>
	"""


def generate_session_results_html(data: dict[str, Any]) -> str:
	race_info = data.get("race_info") or {}
	session_info = data.get("session_info") or {}
	results = data.get("results") or []
	classified_results = [result for result in results if result.get("position") is not None]
	podium_results = classified_results[:3]
	remaining_results = classified_results[3:] + [
		result for result in results if result.get("position") is None
	]
	background = _background_data_uri()

	rows = "".join(
		f"""
		<li class="result-row">
			<span class="result-position">{_text(result.get("position"), "DNF")}</span>
			<span class="result-driver">{_text((result.get("driver_info") or {}).get("full_name"), "Unknown driver")}</span>
			<span class="result-team" style="color: #{_text((result.get("driver_info") or {}).get("team_colour") or "666666").lstrip("#")}">{_text((result.get("driver_info") or {}).get("team_name"), "Unknown team")}</span>
		</li>
		"""
		for result in remaining_results
	)

	return f"""<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=1200, height=1600">
	<title>{_text(race_info.get("meeting_official_name"), "Session results")}</title>
	<style>
		@page {{ size: 1200px 1600px; margin: 0; }}
		* {{ box-sizing: border-box; }}
		html, body {{ width: 1200px; height: 1600px; margin: 0; }}
		body {{
			padding-top: 100px;
			padding-left: 110px;
			color: #17191d;
			font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif;
			background: #eeeeeb url("{background}") center / cover no-repeat;
		}}
		main {{ width: 1080px; min-height: 1470px; padding: 15px 15px 70px; background: rgba(247, 247, 243, .92); }}
		header {{ border-bottom: 7px solid #e10600; padding-bottom: 28px; }}
		.eyebrow {{ color: #e10600; font: 700 22px Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase; }}
		h1 {{ margin: 12px 0 18px; font-size: 58px; line-height: .98; text-transform: uppercase; }}
		.session {{ display: inline-block; padding: 10px 18px; color: white; background: #17191d; font: 700 24px Arial, sans-serif; text-transform: uppercase; }}
		h2 {{ margin: 38px 0 20px; font-size: 30px; text-transform: uppercase; }}
		.podium {{ display: flex; align-items: end; gap: 18px; min-height: 390px; }}
		.podium-card {{ position: relative; flex: 1; min-height: 330px; padding: 22px 18px 20px; text-align: center; background: white; border-top: 16px solid var(--team-colour); box-shadow: 0 6px 0 var(--team-colour); }}
		.place-1 {{ order: 2; min-height: 390px; }} .place-2 {{ order: 1; }} .place-3 {{ order: 3; }}
		.podium-place {{ position: absolute; top: -1px; left: 18px; color: var(--team-colour); font: 700 42px Arial, sans-serif; }}
		.podium-card img {{ width: 170px; height: 170px; object-fit: contain; margin: 18px auto 2px; display: block; }}
		.driver-surname {{ font-size: 28px; line-height: 1; }} .driver-name {{ font: 700 17px Arial, sans-serif; margin-top: 5px; }}
		.team-name {{ margin-top: 12px; font: 700 16px Arial, sans-serif; color: #555; }}
		.results {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 24px; margin: 0; padding: 0; list-style: none; border-top: 3px solid #17191d; }}
		.result-row {{ display: grid; grid-template-columns: 62px 1fr 180px; gap: 12px; align-items: center; min-height: 52px; padding: 8px 10px; border-bottom: 1px solid #c7c7c2; font: 700 18px Arial, sans-serif; }}
		.result-row:nth-child(even) {{ background: rgba(225, 6, 0, .08); }} .result-position {{ color: #e10600; }} .result-team {{ color: #555; font-size: 18px; }}
	</style>
</head>
<body>
	<main>
		<header>
			<div class="eyebrow">Formula 1 / { _text(race_info.get("circuit_short_name"), "Race meeting") } / { _text(session_info.get("session_name"), "Session") } </div>
			<h1>{_text(race_info.get("meeting_official_name"), "Session results")}</h1>
		</header>
		<section>
			<h2>Podium</h2>
			<div class="podium">{"".join(_driver_card(result, index) for index, result in enumerate(podium_results, 1))}</div>
		</section>
		<section>
            <h2>Results</h2>
			<ol class="results">{rows}</ol>
		</section>
	</main>
</body>
</html>"""
