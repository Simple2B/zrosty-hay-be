from bs4 import BeautifulSoup


def get_color_from_svg_icon(svg_icon: str) -> str:
    soup = BeautifulSoup(svg_icon, "html.parser")
    path_element = soup.find("path")
    if path_element:
        return path_element.get("fill", "")
    return ""
