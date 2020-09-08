from .mocks import MockRepository, MockPR, MockReview, MockCommit, MockComment
from random import randint
from gitstats import StatsCollector, PullRequestRepository
from datetime import datetime, timezone, timedelta


class TestStatsCollector:

    def test_no_prs(self):
        expected_prs = []
        repository = MockRepository(expected_prs)
        pullRequestRepository = PullRequestRepository(repository)
        end = datetime.now(timezone.utc) + timedelta(days=7)
        start = datetime.now(timezone.utc) - timedelta(days=7)

        collector = StatsCollector(pullRequestRepository, start=start, end=end)

        assert len(collector.getPRs()) == 0
        assert len(collector.getReviews()) == 0
        assert len(collector.getComments()) == 0
        assert len(collector.getCommits()) == 0

    def test_collects_prs(self):
        expected_commits = []
        expected_reviews = []
        expected_review_comments = []
        expected_issue_comments = []
        expected_prs = []

        for i in range(0, 3):
            expected_commits.append(
                [MockCommit() for i in range(0, randint(0, 10))])
            expected_reviews.append(
                [MockReview() for i in range(0, randint(0, 10))])
            expected_review_comments.append(
                [MockComment() for i in range(0, randint(0, 10))])
            expected_issue_comments.append(
                [MockComment() for i in range(0, randint(0, 10))])
            expected_prs.append(
                MockPR(commits=expected_commits[i],
                       reviews=expected_reviews[i],
                       review_comments=expected_review_comments[i],
                       issue_comments=expected_issue_comments[i]))
        repository = MockRepository(expected_prs)
        pullRequestRepository = PullRequestRepository(repository)

        end = datetime.now(timezone.utc) + timedelta(days=7)
        start = datetime.now(timezone.utc) - timedelta(days=7)

        collector = StatsCollector(pullRequestRepository, start=start, end=end)
        prs = collector.getPRs()
        reviews = collector.getReviews()
        comments = collector.getComments()
        commits = collector.getCommits()
        assert len(prs) == len(expected_prs)
        assert len(reviews) == sum([len(e) for e in expected_reviews])
        assert len(comments) == sum([
            len(e) for e in expected_issue_comments
        ]) + sum([len(e) for e in expected_review_comments])
        assert len(commits) == sum([len(e) for e in expected_commits])

    def test_default_end(self):
        default_end = StatsCollector.default_end()
        now = datetime.utcnow()
        assert default_end < now
        assert default_end.weekday() == 4
        assert (now - default_end).days < 7
        assert default_end.time().isoformat() == "00:00:00"
