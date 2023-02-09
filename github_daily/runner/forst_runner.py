import os

from rich.markdown import Markdown
from rich import print
from rich.table import Table
from github_daily.runner.base_runner import BaseRunner
from github_daily.forst import Forst
from github_daily.config import GTD_LABEL_LIST, REPO_NAME, TIMEZONE

import pendulum


class ForstRunner(BaseRunner):
    """
    TODO
    1. - [ ] show table.
    2. - [ ] sync today
    3. - [ ] show summary
    4. - [ ] support yesterday
    """
    def __init__(self, show_name):
        super().__init__()
        email = os.getenv("FORST_EMAIL")
        password = os.getenv("FORST_PASSWORD")
        github_token = os.getenv("GITHUB_TOKEN")
        # login and make all plants
        self.forst = Forst(email, password, github_token, REPO_NAME)
        self.forst.login()
        self.forst.make_plants_data()
        self.today = pendulum.now(TIMEZONE)
        self.show_name = show_name

    def show(self):
        today_table = self.forst.make_plants_body(self.today)
        table = Table(title="Forst Table Today")
        table.add_column("Tag", style="cyan", no_wrap=True)
        table.add_column("Times", justify="right", style="green")
        for t in today_table.splitlines()[3:]:
            content_list = t.split("|")
            table.add_row(content_list[1], content_list[2].strip())
        print(table)

    def sync(self):
        self.forst.make_daily_table()
        print(Markdown("---\r\n" + "## Forst after sync"))
        self.show()