# -*- coding: utf-8 -*-
bl_info = {
    "name": "Сборщик костей",
    "author": "Peligrosso087",
    "version": (1, 0, 0),
    "blender": (5, 2, 0),
    "location": "View3D > Sidebar > Сборщик",
    "description": "Автоматически собирает кости арматуры в коллекции и создаёт скелет",
    "category": "Rigging",
}

import base64
import json
import re
import bpy
from bpy.props import BoolProperty
from bpy.types import Operator, Panel, PropertyGroup


PACK = json.loads(base64.b64decode("eyJsb2NhbGUiOiJydSIsImNvbnZlbnRpb24iOiJibGVuZGVyIiwic2NoZW1hIjoiYW5hdG9taWNhbCIsInRlbXBsYXRlIjoiaHVtYW5vaWQiLCJvcHRpb25zIjp7ImNvbG9yQm9uZXMiOnRydWUsImhpZGVNZWNoYW5pc20iOnRydWUsInJlYXNzaWduIjp0cnVlLCJnZW5lcmF0ZUlrIjpmYWxzZSwiaW5jbHVkZUZpbmdlcnMiOnRydWUsImluY2x1ZGVGYWNlIjpmYWxzZSwiaGVpZ2h0IjoxLjh9LCJjb2xsZWN0aW9ucyI6W3siaWQiOiJyb290IiwibmFtZSI6ItCa0L7RgNC10L3RjCIsImNvbG9yIjpbMC40NSwwLjQ0LDAuNDJdLCJ2aXNpYmxlIjp0cnVlfSx7ImlkIjoic3BpbmUiLCJuYW1lIjoi0J/QvtC30LLQvtC90L7Rh9C90LjQuiIsImNvbG9yIjpbMC44MywwLjgsMC43Nl0sInZpc2libGUiOnRydWV9LHsiaWQiOiJoZWFkIiwibmFtZSI6ItCT0L7Qu9C+0LLQsCIsImNvbG9yIjpbMC44OCwwLjg1LDAuOF0sInZpc2libGUiOnRydWV9LHsiaWQiOiJhcm1fbCIsIm5hbWUiOiLQoNGD0LrQsCBMIiwiY29sb3IiOlswLjYsMC42OSwwLjddLCJ2aXNpYmxlIjp0cnVlfSx7ImlkIjoiYXJtX3IiLCJuYW1lIjoi0KDRg9C60LAgUiIsImNvbG9yIjpbMC41NiwwLjYzLDAuNzJdLCJ2aXNpYmxlIjp0cnVlfSx7ImlkIjoiaGFuZF9sIiwibmFtZSI6ItCa0LjRgdGC0YwgTCIsImNvbG9yIjpbMC41NCwwLjYsMC41Nl0sInZpc2libGUiOnRydWV9LHsiaWQiOiJoYW5kX3IiLCJuYW1lIjoi0JrQuNGB0YLRjCBSIiwiY29sb3IiOlswLjUsMC41OCwwLjU0XSwidmlzaWJsZSI6dHJ1ZX0seyJpZCI6ImxlZ19sIiwibmFtZSI6ItCd0L7Qs9CwIEwiLCJjb2xvciI6WzAuNzEsMC42NiwwLjU5XSwidmlzaWJsZSI6dHJ1ZX0seyJpZCI6ImxlZ19yIiwibmFtZSI6ItCd0L7Qs9CwIFIiLCJjb2xvciI6WzAuNjYsMC42LDAuNTNdLCJ2aXNpYmxlIjp0cnVlfSx7ImlkIjoiaWsiLCJuYW1lIjoiSUsiLCJjb2xvciI6WzAuNDgsMC41NCwwLjUzXSwidmlzaWJsZSI6ZmFsc2V9LHsiaWQiOiJtY2giLCJuYW1lIjoi0JzQtdGF0LDQvdC40LrQsCIsImNvbG9yIjpbMC40MiwwLjQxLDAuMzldLCJ2aXNpYmxlIjpmYWxzZX0seyJpZCI6InVuc29ydGVkIiwibmFtZSI6ItCx0LXQtyDQs9GA0YPQv9C/0YsiLCJjb2xvciI6WzAuNDgsMC40NywwLjQ1XSwidmlzaWJsZSI6dHJ1ZX1dLCJydWxlcyI6W3siY29sbGVjdGlvbiI6InJvb3QiLCJwYXR0ZXJuIjoiXnJvb3QkfChefF98OnxcXC58LSlyb290KCR8X3w6fFxcLnwtKXxeYmlwJHxeYXJtYXR1cmUkIn0seyJjb2xsZWN0aW9uIjoiaWsiLCJwYXR0ZXJuIjoiKF58X3w6fFxcLnwtKShpa3xwb2xlfHRhcmdldCkoX3w6fFxcLnwtfCQpfGlrW18tXXxfaWskfHBvbGUifSx7ImNvbGxlY3Rpb24iOiJtY2giLCJwYXR0ZXJuIjoiKF58X3w6fFxcLnwtKShtY2h8dGd0fGludCkoX3w6fFxcLnwtKXxtY2hbLV9dIn0seyJjb2xsZWN0aW9uIjoiaGFuZF9sIiwicGF0dGVybiI6Iih0aHVtYnxpbmRleHxtaWRkbGV8cmluZ3xwaW5reXxmaW5nZXIpLioobCR8XFwubCR8X2wkfGxlZnQpfGxlZnQuKih0aHVtYnxpbmRleHxtaWRkbGV8cmluZ3xwaW5reXxmaW5nZXJ8aGFuZCkifSx7ImNvbGxlY3Rpb24iOiJoYW5kX3IiLCJwYXR0ZXJuIjoiKHRodW1ifGluZGV4fG1pZGRsZXxyaW5nfHBpbmt5fGZpbmdlcikuKihyJHxcXC5yJHxfciR8cmlnaHQpfHJpZ2h0LioodGh1bWJ8aW5kZXh8bWlkZGxlfHJpbmd8cGlua3l8ZmluZ2VyfGhhbmQpIn0seyJjb2xsZWN0aW9uIjoiYXJtX2wiLCJwYXR0ZXJuIjoiKHNob3VsZGVyfGNsYXZpY2xlfGFybXxmb3JlYXJtfGhhbmQpLioobCR8XFwubCR8X2wkKXxsZWZ0Liooc2hvdWxkZXJ8Y2xhdmljbGV8YXJtfGZvcmVhcm18aGFuZCl8d2luZy4qKF9sfFxcLmx8bGVmdCkifSx7ImNvbGxlY3Rpb24iOiJhcm1fciIsInBhdHRlcm4iOiIoc2hvdWxkZXJ8Y2xhdmljbGV8YXJtfGZvcmVhcm18aGFuZCkuKihyJHxcXC5yJHxfciQpfHJpZ2h0Liooc2hvdWxkZXJ8Y2xhdmljbGV8YXJtfGZvcmVhcm18aGFuZCl8d2luZy4qKF9yfFxcLnJ8cmlnaHQpIn0seyJjb2xsZWN0aW9uIjoibGVnX2wiLCJwYXR0ZXJuIjoiKHRoaWdofHVwbGVnfGxlZ3xzaGlufGNhbGZ8Zm9vdHx0b2V8YmFsbCkuKihsJHxcXC5sJHxfbCQpfGxlZnQuKih1cGxlZ3xsZWd8dGhpZ2h8c2hpbnxjYWxmfGZvb3R8dG9lKSJ9LHsiY29sbGVjdGlvbiI6ImxlZ19yIiwicGF0dGVybiI6Iih0aGlnaHx1cGxlZ3xsZWd8c2hpbnxjYWxmfGZvb3R8dG9lfGJhbGwpLioociR8XFwuciR8X3IkKXxyaWdodC4qKHVwbGVnfGxlZ3x0aGlnaHxzaGlufGNhbGZ8Zm9vdHx0b2UpIn0seyJjb2xsZWN0aW9uIjoiaGVhZCIsInBhdHRlcm4iOiJoZWFkfG5lY2t8amF3fGV5ZXxza3VsbHxmYWNlIn0seyJjb2xsZWN0aW9uIjoic3BpbmUiLCJwYXR0ZXJuIjoic3BpbmV8cGVsdmlzfGhpcHN8dG9yc298Y2hlc3R8dGFpbHxoaXAifV0sInJpZyI6W3siaWQiOiJyb290IiwibmFtZSI6InJvb3QiLCJoZWFkIjpbMCwwLDBdLCJ0YWlsIjpbMCwwLDAuMDhdLCJwYXJlbnQiOm51bGwsImNvbm5lY3QiOmZhbHNlLCJyb2xsIjowLCJkZWZvcm0iOmZhbHNlLCJjb2xsZWN0aW9uIjoicm9vdCJ9LHsiaWQiOiJwZWx2aXMiLCJuYW1lIjoicGVsdmlzIiwiaGVhZCI6WzAsMCwwLjk0XSwidGFpbCI6WzAsMCwxLjA0XSwicGFyZW50Ijoicm9vdCIsImNvbm5lY3QiOmZhbHNlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJzcGluZSJ9LHsiaWQiOiJzcGluZV8wMSIsIm5hbWUiOiJzcGluZV8wMSIsImhlYWQiOlswLDAsMS4wNF0sInRhaWwiOlswLDAsMS4yXSwicGFyZW50IjoicGVsdmlzIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoic3BpbmUifSx7ImlkIjoic3BpbmVfMDIiLCJuYW1lIjoic3BpbmVfMDIiLCJoZWFkIjpbMCwwLDEuMl0sInRhaWwiOlswLDAsMS4zNl0sInBhcmVudCI6InNwaW5lXzAxIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoic3BpbmUifSx7ImlkIjoic3BpbmVfMDMiLCJuYW1lIjoic3BpbmVfMDMiLCJoZWFkIjpbMCwwLDEuMzZdLCJ0YWlsIjpbMCwwLDEuNV0sInBhcmVudCI6InNwaW5lXzAyIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoic3BpbmUifSx7ImlkIjoibmVjayIsIm5hbWUiOiJuZWNrIiwiaGVhZCI6WzAsMCwxLjVdLCJ0YWlsIjpbMCwwLDEuNjJdLCJwYXJlbnQiOiJzcGluZV8wMyIsImNvbm5lY3QiOnRydWUsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImhlYWQifSx7ImlkIjoiaGVhZCIsIm5hbWUiOiJoZWFkIiwiaGVhZCI6WzAsMCwxLjYyXSwidGFpbCI6WzAsMCwxLjhdLCJwYXJlbnQiOiJuZWNrIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGVhZCJ9LHsiaWQiOiJzaG91bGRlcl9MIiwibmFtZSI6InNob3VsZGVyX0wiLCJoZWFkIjpbMC4wNCwwLDEuNDhdLCJ0YWlsIjpbMC4xNiwwLDEuNV0sInBhcmVudCI6InNwaW5lXzAzIiwiY29ubmVjdCI6ZmFsc2UsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImFybV9sIn0seyJpZCI6InVwcGVyX2FybV9MIiwibmFtZSI6InVwcGVyX2FybV9MIiwiaGVhZCI6WzAuMTYsMCwxLjVdLCJ0YWlsIjpbMC40NiwwLDEuNV0sInBhcmVudCI6InNob3VsZGVyX0wiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJhcm1fbCJ9LHsiaWQiOiJmb3JlYXJtX0wiLCJuYW1lIjoiZm9yZWFybV9MIiwiaGVhZCI6WzAuNDYsMCwxLjVdLCJ0YWlsIjpbMC43NCwwLDEuNV0sInBhcmVudCI6InVwcGVyX2FybV9MIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiYXJtX2wifSx7ImlkIjoiaGFuZF9MIiwibmFtZSI6ImhhbmRfTCIsImhlYWQiOlswLjc0LDAsMS41XSwidGFpbCI6WzAuODYsMCwxLjVdLCJwYXJlbnQiOiJmb3JlYXJtX0wiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX2wifSx7ImlkIjoidGhpZ2hfTCIsIm5hbWUiOiJ0aGlnaF9MIiwiaGVhZCI6WzAuMDksMCwwLjk0XSwidGFpbCI6WzAuMSwwLjAyLDAuNV0sInBhcmVudCI6InBlbHZpcyIsImNvbm5lY3QiOmZhbHNlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJsZWdfbCJ9LHsiaWQiOiJzaGluX0wiLCJuYW1lIjoic2hpbl9MIiwiaGVhZCI6WzAuMSwwLjAyLDAuNV0sInRhaWwiOlswLjEsMCwwLjFdLCJwYXJlbnQiOiJ0aGlnaF9MIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoibGVnX2wifSx7ImlkIjoiZm9vdF9MIiwibmFtZSI6ImZvb3RfTCIsImhlYWQiOlswLjEsMCwwLjFdLCJ0YWlsIjpbMC4xLC0wLjEyLDAuMDNdLCJwYXJlbnQiOiJzaGluX0wiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJsZWdfbCJ9LHsiaWQiOiJ0b2VfTCIsIm5hbWUiOiJ0b2VfTCIsImhlYWQiOlswLjEsLTAuMTIsMC4wM10sInRhaWwiOlswLjEsLTAuMiwwLjAzXSwicGFyZW50IjoiZm9vdF9MIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoibGVnX2wifSx7ImlkIjoic2hvdWxkZXJfUiIsIm5hbWUiOiJzaG91bGRlcl9SIiwiaGVhZCI6Wy0wLjA0LDAsMS40OF0sInRhaWwiOlstMC4xNiwwLDEuNV0sInBhcmVudCI6InNwaW5lXzAzIiwiY29ubmVjdCI6ZmFsc2UsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImFybV9yIn0seyJpZCI6InVwcGVyX2FybV9SIiwibmFtZSI6InVwcGVyX2FybV9SIiwiaGVhZCI6Wy0wLjE2LDAsMS41XSwidGFpbCI6Wy0wLjQ2LDAsMS41XSwicGFyZW50Ijoic2hvdWxkZXJfUiIsImNvbm5lY3QiOnRydWUsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImFybV9yIn0seyJpZCI6ImZvcmVhcm1fUiIsIm5hbWUiOiJmb3JlYXJtX1IiLCJoZWFkIjpbLTAuNDYsMCwxLjVdLCJ0YWlsIjpbLTAuNzQsMCwxLjVdLCJwYXJlbnQiOiJ1cHBlcl9hcm1fUiIsImNvbm5lY3QiOnRydWUsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImFybV9yIn0seyJpZCI6ImhhbmRfUiIsIm5hbWUiOiJoYW5kX1IiLCJoZWFkIjpbLTAuNzQsMCwxLjVdLCJ0YWlsIjpbLTAuODYsMCwxLjVdLCJwYXJlbnQiOiJmb3JlYXJtX1IiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX3IifSx7ImlkIjoidGhpZ2hfUiIsIm5hbWUiOiJ0aGlnaF9SIiwiaGVhZCI6Wy0wLjA5LDAsMC45NF0sInRhaWwiOlstMC4xLDAuMDIsMC41XSwicGFyZW50IjoicGVsdmlzIiwiY29ubmVjdCI6ZmFsc2UsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImxlZ19yIn0seyJpZCI6InNoaW5fUiIsIm5hbWUiOiJzaGluX1IiLCJoZWFkIjpbLTAuMSwwLjAyLDAuNV0sInRhaWwiOlstMC4xLDAsMC4xXSwicGFyZW50IjoidGhpZ2hfUiIsImNvbm5lY3QiOnRydWUsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImxlZ19yIn0seyJpZCI6ImZvb3RfUiIsIm5hbWUiOiJmb290X1IiLCJoZWFkIjpbLTAuMSwwLDAuMV0sInRhaWwiOlstMC4xLC0wLjEyLDAuMDNdLCJwYXJlbnQiOiJzaGluX1IiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJsZWdfciJ9LHsiaWQiOiJ0b2VfUiIsIm5hbWUiOiJ0b2VfUiIsImhlYWQiOlstMC4xLC0wLjEyLDAuMDNdLCJ0YWlsIjpbLTAuMSwtMC4yLDAuMDNdLCJwYXJlbnQiOiJmb290X1IiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJsZWdfciJ9LHsiaWQiOiJ0aHVtYl8wMV9MIiwibmFtZSI6InRodW1iXzAxX0wiLCJoZWFkIjpbMC44MiwtMC4wNCwxLjQxXSwidGFpbCI6WzAuODY1LC0wLjA0LDEuMzldLCJwYXJlbnQiOiJoYW5kX0wiLCJjb25uZWN0IjpmYWxzZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9sIn0seyJpZCI6InRodW1iXzAyX0wiLCJuYW1lIjoidGh1bWJfMDJfTCIsImhlYWQiOlswLjg2NSwtMC4wNCwxLjM5XSwidGFpbCI6WzAuOTA5OTk5OTk5OTk5OTk5OSwtMC4wNCwxLjM2OTk5OTk5OTk5OTk5OTldLCJwYXJlbnQiOiJ0aHVtYl8wMV9MIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9sIn0seyJpZCI6InRodW1iXzAzX0wiLCJuYW1lIjoidGh1bWJfMDNfTCIsImhlYWQiOlswLjkwOTk5OTk5OTk5OTk5OTksLTAuMDQsMS4zNjk5OTk5OTk5OTk5OTk5XSwidGFpbCI6WzAuOTU1LC0wLjA0LDEuMzQ5OTk5OTk5OTk5OTk5OV0sInBhcmVudCI6InRodW1iXzAyX0wiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX2wifSx7ImlkIjoiaW5kZXhfMDFfTCIsIm5hbWUiOiJpbmRleF8wMV9MIiwiaGVhZCI6WzAuODYsLTAuMDIsMS41OF0sInRhaWwiOlswLjkxLC0wLjAyLDEuNThdLCJwYXJlbnQiOiJoYW5kX0wiLCJjb25uZWN0IjpmYWxzZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9sIn0seyJpZCI6ImluZGV4XzAyX0wiLCJuYW1lIjoiaW5kZXhfMDJfTCIsImhlYWQiOlswLjkxLC0wLjAyLDEuNThdLCJ0YWlsIjpbMC45NiwtMC4wMiwxLjU4XSwicGFyZW50IjoiaW5kZXhfMDFfTCIsImNvbm5lY3QiOnRydWUsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImhhbmRfbCJ9LHsiaWQiOiJpbmRleF8wM19MIiwibmFtZSI6ImluZGV4XzAzX0wiLCJoZWFkIjpbMC45NiwtMC4wMiwxLjU4XSwidGFpbCI6WzEuMDEsLTAuMDIsMS41OF0sInBhcmVudCI6ImluZGV4XzAyX0wiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX2wifSx7ImlkIjoibWlkZGxlXzAxX0wiLCJuYW1lIjoibWlkZGxlXzAxX0wiLCJoZWFkIjpbMC44NywwLDEuNTNdLCJ0YWlsIjpbMC45MiwwLDEuNTNdLCJwYXJlbnQiOiJoYW5kX0wiLCJjb25uZWN0IjpmYWxzZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9sIn0seyJpZCI6Im1pZGRsZV8wMl9MIiwibmFtZSI6Im1pZGRsZV8wMl9MIiwiaGVhZCI6WzAuOTIsMCwxLjUzXSwidGFpbCI6WzAuOTcsMCwxLjUzXSwicGFyZW50IjoibWlkZGxlXzAxX0wiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX2wifSx7ImlkIjoibWlkZGxlXzAzX0wiLCJuYW1lIjoibWlkZGxlXzAzX0wiLCJoZWFkIjpbMC45NywwLDEuNTNdLCJ0YWlsIjpbMS4wMiwwLDEuNTNdLCJwYXJlbnQiOiJtaWRkbGVfMDJfTCIsImNvbm5lY3QiOnRydWUsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImhhbmRfbCJ9LHsiaWQiOiJyaW5nXzAxX0wiLCJuYW1lIjoicmluZ18wMV9MIiwiaGVhZCI6WzAuODYsMC4wMiwxLjQ3XSwidGFpbCI6WzAuOTEsMC4wMiwxLjQ3XSwicGFyZW50IjoiaGFuZF9MIiwiY29ubmVjdCI6ZmFsc2UsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImhhbmRfbCJ9LHsiaWQiOiJyaW5nXzAyX0wiLCJuYW1lIjoicmluZ18wMl9MIiwiaGVhZCI6WzAuOTEsMC4wMiwxLjQ3XSwidGFpbCI6WzAuOTYsMC4wMiwxLjQ3XSwicGFyZW50IjoicmluZ18wMV9MIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9sIn0seyJpZCI6InJpbmdfMDNfTCIsIm5hbWUiOiJyaW5nXzAzX0wiLCJoZWFkIjpbMC45NiwwLjAyLDEuNDddLCJ0YWlsIjpbMS4wMSwwLjAyLDEuNDddLCJwYXJlbnQiOiJyaW5nXzAyX0wiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX2wifSx7ImlkIjoicGlua3lfMDFfTCIsIm5hbWUiOiJwaW5reV8wMV9MIiwiaGVhZCI6WzAuODQsMC4wNCwxLjQxXSwidGFpbCI6WzAuODksMC4wNCwxLjQxXSwicGFyZW50IjoiaGFuZF9MIiwiY29ubmVjdCI6ZmFsc2UsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImhhbmRfbCJ9LHsiaWQiOiJwaW5reV8wMl9MIiwibmFtZSI6InBpbmt5XzAyX0wiLCJoZWFkIjpbMC44OSwwLjA0LDEuNDFdLCJ0YWlsIjpbMC45NCwwLjA0LDEuNDFdLCJwYXJlbnQiOiJwaW5reV8wMV9MIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9sIn0seyJpZCI6InBpbmt5XzAzX0wiLCJuYW1lIjoicGlua3lfMDNfTCIsImhlYWQiOlswLjk0LDAuMDQsMS40MV0sInRhaWwiOlswLjk5LDAuMDQsMS40MV0sInBhcmVudCI6InBpbmt5XzAyX0wiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX2wifSx7ImlkIjoidGh1bWJfMDFfUiIsIm5hbWUiOiJ0aHVtYl8wMV9SIiwiaGVhZCI6Wy0wLjgyLC0wLjA0LDEuNDFdLCJ0YWlsIjpbLTAuODY1LC0wLjA0LDEuMzldLCJwYXJlbnQiOiJoYW5kX1IiLCJjb25uZWN0IjpmYWxzZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9yIn0seyJpZCI6InRodW1iXzAyX1IiLCJuYW1lIjoidGh1bWJfMDJfUiIsImhlYWQiOlstMC44NjUsLTAuMDQsMS4zOV0sInRhaWwiOlstMC45MDk5OTk5OTk5OTk5OTk5LC0wLjA0LDEuMzY5OTk5OTk5OTk5OTk5OV0sInBhcmVudCI6InRodW1iXzAxX1IiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX3IifSx7ImlkIjoidGh1bWJfMDNfUiIsIm5hbWUiOiJ0aHVtYl8wM19SIiwiaGVhZCI6Wy0wLjkwOTk5OTk5OTk5OTk5OTksLTAuMDQsMS4zNjk5OTk5OTk5OTk5OTk5XSwidGFpbCI6Wy0wLjk1NSwtMC4wNCwxLjM0OTk5OTk5OTk5OTk5OTldLCJwYXJlbnQiOiJ0aHVtYl8wMl9SIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9yIn0seyJpZCI6ImluZGV4XzAxX1IiLCJuYW1lIjoiaW5kZXhfMDFfUiIsImhlYWQiOlstMC44NiwtMC4wMiwxLjU4XSwidGFpbCI6Wy0wLjkxLC0wLjAyLDEuNThdLCJwYXJlbnQiOiJoYW5kX1IiLCJjb25uZWN0IjpmYWxzZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9yIn0seyJpZCI6ImluZGV4XzAyX1IiLCJuYW1lIjoiaW5kZXhfMDJfUiIsImhlYWQiOlstMC45MSwtMC4wMiwxLjU4XSwidGFpbCI6Wy0wLjk2LC0wLjAyLDEuNThdLCJwYXJlbnQiOiJpbmRleF8wMV9SIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9yIn0seyJpZCI6ImluZGV4XzAzX1IiLCJuYW1lIjoiaW5kZXhfMDNfUiIsImhlYWQiOlstMC45NiwtMC4wMiwxLjU4XSwidGFpbCI6Wy0xLjAxLC0wLjAyLDEuNThdLCJwYXJlbnQiOiJpbmRleF8wMl9SIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9yIn0seyJpZCI6Im1pZGRsZV8wMV9SIiwibmFtZSI6Im1pZGRsZV8wMV9SIiwiaGVhZCI6Wy0wLjg3LDAsMS41M10sInRhaWwiOlstMC45MiwwLDEuNTNdLCJwYXJlbnQiOiJoYW5kX1IiLCJjb25uZWN0IjpmYWxzZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9yIn0seyJpZCI6Im1pZGRsZV8wMl9SIiwibmFtZSI6Im1pZGRsZV8wMl9SIiwiaGVhZCI6Wy0wLjkyLDAsMS41M10sInRhaWwiOlstMC45NywwLDEuNTNdLCJwYXJlbnQiOiJtaWRkbGVfMDFfUiIsImNvbm5lY3QiOnRydWUsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImhhbmRfciJ9LHsiaWQiOiJtaWRkbGVfMDNfUiIsIm5hbWUiOiJtaWRkbGVfMDNfUiIsImhlYWQiOlstMC45NywwLDEuNTNdLCJ0YWlsIjpbLTEuMDIsMCwxLjUzXSwicGFyZW50IjoibWlkZGxlXzAyX1IiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX3IifSx7ImlkIjoicmluZ18wMV9SIiwibmFtZSI6InJpbmdfMDFfUiIsImhlYWQiOlstMC44NiwwLjAyLDEuNDddLCJ0YWlsIjpbLTAuOTEsMC4wMiwxLjQ3XSwicGFyZW50IjoiaGFuZF9SIiwiY29ubmVjdCI6ZmFsc2UsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImhhbmRfciJ9LHsiaWQiOiJyaW5nXzAyX1IiLCJuYW1lIjoicmluZ18wMl9SIiwiaGVhZCI6Wy0wLjkxLDAuMDIsMS40N10sInRhaWwiOlstMC45NiwwLjAyLDEuNDddLCJwYXJlbnQiOiJyaW5nXzAxX1IiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX3IifSx7ImlkIjoicmluZ18wM19SIiwibmFtZSI6InJpbmdfMDNfUiIsImhlYWQiOlstMC45NiwwLjAyLDEuNDddLCJ0YWlsIjpbLTEuMDEsMC4wMiwxLjQ3XSwicGFyZW50IjoicmluZ18wMl9SIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9yIn0seyJpZCI6InBpbmt5XzAxX1IiLCJuYW1lIjoicGlua3lfMDFfUiIsImhlYWQiOlstMC44NCwwLjA0LDEuNDFdLCJ0YWlsIjpbLTAuODksMC4wNCwxLjQxXSwicGFyZW50IjoiaGFuZF9SIiwiY29ubmVjdCI6ZmFsc2UsInJvbGwiOjAsImRlZm9ybSI6dHJ1ZSwiY29sbGVjdGlvbiI6ImhhbmRfciJ9LHsiaWQiOiJwaW5reV8wMl9SIiwibmFtZSI6InBpbmt5XzAyX1IiLCJoZWFkIjpbLTAuODksMC4wNCwxLjQxXSwidGFpbCI6Wy0wLjk0LDAuMDQsMS40MV0sInBhcmVudCI6InBpbmt5XzAxX1IiLCJjb25uZWN0Ijp0cnVlLCJyb2xsIjowLCJkZWZvcm0iOnRydWUsImNvbGxlY3Rpb24iOiJoYW5kX3IifSx7ImlkIjoicGlua3lfMDNfUiIsIm5hbWUiOiJwaW5reV8wM19SIiwiaGVhZCI6Wy0wLjk0LDAuMDQsMS40MV0sInRhaWwiOlstMC45OSwwLjA0LDEuNDFdLCJwYXJlbnQiOiJwaW5reV8wMl9SIiwiY29ubmVjdCI6dHJ1ZSwicm9sbCI6MCwiZGVmb3JtIjp0cnVlLCJjb2xsZWN0aW9uIjoiaGFuZF9yIn1dLCJpayI6W119").decode("utf-8"))


def _armature(context):
    obj = context.view_layer.objects.active
    if obj is None or obj.type != "ARMATURE":
        return None
    return obj


def _get_or_create_collection(arm, name):
    coll = arm.collections.get(name)
    if coll is None:
        coll = arm.collections.new(name)
    return coll


def _classify(name, rules):
    for rule in rules:
        try:
            if re.search(rule["pattern"], name, re.IGNORECASE):
                return rule["collection"]
        except re.error:
            continue
    return "unsorted"


def _colorize(obj, bone_name, rgb):
    bone = obj.data.bones.get(bone_name)
    pose = obj.pose.bones.get(bone_name) if obj.pose else None
    for target in (bone, pose):
        if target is None or not hasattr(target, "color"):
            continue
        target.color.palette = "CUSTOM"
        target.color.custom.normal = rgb
        target.color.custom.select = (
            min(1.0, rgb[0] + 0.22),
            min(1.0, rgb[1] + 0.22),
            min(1.0, rgb[2] + 0.22),
        )
        target.color.custom.active = (1.0, 1.0, 1.0)


def _ensure_pose(obj):
    prev = obj.mode
    if prev == "EDIT":
        bpy.ops.object.mode_set(mode="POSE")
    return prev


def _restore_mode(prev):
    if prev and prev != bpy.context.object.mode:
        try:
            bpy.ops.object.mode_set(mode=prev)
        except Exception:
            pass


def collect_bones(obj, settings):
    arm = obj.data
    prev = _ensure_pose(obj)
    managed = {c["name"] for c in PACK["collections"]}
    id_to_coll = {}
    id_to_color = {}
    for spec in PACK["collections"]:
        coll = _get_or_create_collection(arm, spec["name"])
        if spec["id"] in ("mch", "ik", "org"):
            coll.is_visible = not settings.hide_mech
        id_to_coll[spec["id"]] = coll
        id_to_color[spec["id"]] = tuple(spec["color"])

    used = set()
    assigned = 0
    for bone in arm.bones:
        cid = _classify(bone.name, PACK["rules"])
        coll = id_to_coll.get(cid) or id_to_coll.get("unsorted")
        if coll is None:
            continue
        if settings.reassign:
            for existing in list(getattr(bone, "collections", [])):
                if existing.name in managed:
                    existing.unassign(bone)
        coll.assign(bone)
        used.add(coll.name)
        if settings.color_bones:
            rgb = id_to_color.get(cid) or id_to_color.get("unsorted")
            if rgb:
                _colorize(obj, bone.name, rgb)
        assigned += 1

    if hasattr(arm, "show_bone_colors"):
        arm.show_bone_colors = bool(settings.color_bones)
    _restore_mode(prev)
    return assigned, len(used)


def generate_rig(context):
    name = "CollectorRig"
    arm_data = bpy.data.armatures.new(name)
    obj = bpy.data.objects.new(name, arm_data)
    context.collection.objects.link(obj)
    obj.show_in_front = True
    obj.location = context.scene.cursor.location
    arm_data.display_type = "OCTAHEDRAL"

    for other in list(context.selected_objects):
        other.select_set(False)
    obj.select_set(True)
    context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode="EDIT")
    for bone in list(arm_data.edit_bones):
        arm_data.edit_bones.remove(bone)

    created = {}
    for spec in PACK["rig"]:
        eb = arm_data.edit_bones.new(spec["name"])
        eb.head = spec["head"]
        eb.tail = spec["tail"]
        eb.roll = spec.get("roll", 0.0)
        eb.use_deform = spec.get("deform", True)
        created[spec["name"]] = eb

    name_by_id = {spec["id"]: spec["name"] for spec in PACK["rig"]}
    for spec in PACK["rig"]:
        parent_id = spec.get("parent")
        if not parent_id:
            continue
        parent_name = name_by_id.get(parent_id)
        if not parent_name or parent_name not in created:
            continue
        created[spec["name"]].parent = created[parent_name]
        created[spec["name"]].use_connect = bool(spec.get("connect"))

    bpy.ops.object.mode_set(mode="POSE")
    dummy = type("S", (), {"reassign": True, "color_bones": True, "hide_mech": PACK["options"]["hideMechanism"]})()
    collect_bones(obj, dummy)

    for constraint in PACK.get("ik", []):
        pb = obj.pose.bones.get(constraint["bone"])
        if pb is None:
            continue
        con = pb.constraints.new("IK")
        con.target = obj
        con.subtarget = constraint["target"]
        con.chain_count = int(constraint.get("chain", 2))
        pole = constraint.get("pole")
        if pole:
            con.pole_target = obj
            con.pole_subtarget = pole
            con.pole_angle = float(constraint.get("poleAngle", 0.0))

    bpy.ops.object.mode_set(mode="OBJECT")
    return obj, len(PACK["rig"])


class COLLECTOR_Settings(PropertyGroup):
    reassign: BoolProperty(name="Переназначить", default=True)
    color_bones: BoolProperty(name="Окрасить кости", default=True)
    hide_mech: BoolProperty(name="Скрыть механизмы", default=True)


class COLLECTOR_OT_collect(Operator):
    bl_idname = "collector.collect_bones"
    bl_label = "Собрать кости"
    bl_description = "Автоматически собирает кости арматуры в коллекции и создаёт скелет"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = _armature(context)
        if obj is None:
            self.report({"ERROR"}, "Выделите объект-арматуру")
            return {"CANCELLED"}
        n, c = collect_bones(obj, context.scene.collector)
        self.report({"INFO"}, "Собрано {n} костей в {c} коллекций".replace("{n}", str(n)).replace("{c}", str(c)))
        return {"FINISHED"}


class COLLECTOR_OT_generate(Operator):
    bl_idname = "collector.generate_rig"
    bl_label = "Создать скелет"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj, n = generate_rig(context)
        self.report({"INFO"}, "Скелет создан: {n} костей".replace("{n}", str(n)))
        return {"FINISHED"}


class COLLECTOR_OT_clear(Operator):
    bl_idname = "collector.clear_collections"
    bl_label = "Очистить коллекции"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = _armature(context)
        if obj is None:
            self.report({"ERROR"}, "Выделите объект-арматуру")
            return {"CANCELLED"}
        prev = _ensure_pose(obj)
        arm = obj.data
        managed = {c["name"] for c in PACK["collections"]}
        for bone in arm.bones:
            for coll in list(getattr(bone, "collections", [])):
                if coll.name in managed:
                    coll.unassign(bone)
        for spec in PACK["collections"]:
            coll = arm.collections.get(spec["name"])
            if coll is not None:
                try:
                    arm.collections.remove(coll)
                except Exception:
                    pass
        _restore_mode(prev)
        self.report({"INFO"}, "Коллекции сборщика удалены")
        return {"FINISHED"}


class COLLECTOR_OT_select(Operator):
    bl_idname = "collector.select_collection"
    bl_label = "Выделить коллекцию"
    bl_options = {"REGISTER", "UNDO"}
    collection: bpy.props.StringProperty()

    def execute(self, context):
        obj = _armature(context)
        if obj is None:
            self.report({"ERROR"}, "Выделите объект-арматуру")
            return {"CANCELLED"}
        prev = _ensure_pose(obj)
        bpy.ops.pose.select_all(action="DESELECT")
        for bone in obj.data.bones:
            names = [c.name for c in getattr(bone, "collections", [])]
            if self.collection in names:
                bone.select = True
        _restore_mode(prev)
        return {"FINISHED"}


class COLLECTOR_PT_panel(Panel):
    bl_label = "Сборщик"
    bl_idname = "COLLECTOR_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Сборщик"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.collector
        layout.operator("collector.collect_bones", icon="BONE_DATA")
        layout.operator("collector.generate_rig", icon="ARMATURE_DATA")
        col = layout.column(align=True)
        col.prop(settings, "reassign")
        col.prop(settings, "color_bones")
        col.prop(settings, "hide_mech")
        layout.separator()
        box = layout.box()
        box.label(text="Коллекции")
        for spec in PACK["collections"]:
            row = box.row(align=True)
            op = row.operator("collector.select_collection", text=spec["name"])
            op.collection = spec["name"]
        layout.operator("collector.clear_collections", icon="X")


CLASSES = (
    COLLECTOR_Settings,
    COLLECTOR_OT_collect,
    COLLECTOR_OT_generate,
    COLLECTOR_OT_clear,
    COLLECTOR_OT_select,
    COLLECTOR_PT_panel,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.collector = bpy.props.PointerProperty(type=COLLECTOR_Settings)


def unregister():
    del bpy.types.Scene.collector
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    try:
        unregister()
    except Exception:
        pass
    register()
