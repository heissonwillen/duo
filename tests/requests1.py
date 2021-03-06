from . import state

from requests_html import HTML, HTMLSession


def get_user_info(username):
	response_html = HTMLSession().get(
		f"http://duome.eu/{username}",
		headers={"Cookie": f"PHPSESSID=4dfcaa82cc994ccc6b18d5f906a197bd",},
	).html

	streak = response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[3]", first=True).text
	if "#" in streak:
		streak = response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[3]/span[1]", first=True).text

	return {
		"username": username,
		"total_xp": response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[1]", first=True).text.replace(" XP", ""),
		"total_streak": streak
	}

def scrape():
	users = state.load()

	for user_index, user in enumerate(users):
		users[user_index] = get_user_info(user["username"])
		print(f"Getting info from duome.eu ({(100*(user_index+1)/len(users)):.1f}% complete)")

	state.save(users)


if __name__ == '__main__':
	pass
