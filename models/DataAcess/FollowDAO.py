class FollowDAO:
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "follow"

	def follow(self, uid, bid):
		q = self.db.query("INSERT INTO @table (`uid`, `bid`) VALUES ({}, {})"
							.format(uid, bid))
		self.db.commit()

		return q

	def unfollow(self, uid, bid):
		q = self.db.query("DELETE FROM @table WHERE (uid = {} and bid = {})"
							.format(uid, bid))
		self.db.commit()

		return q

	def get_following_bids(self, uid):
		q = self.db.query('select bid from @table where uid={}'.format(uid))
		raw = q.fetchall()
		if raw:
			bids = [ bid[0] for bid in raw ]
			return bids
		return []

	def get_follower(self, bid):
		q = self.db.query('select uid from @table where bid={}'.format(bid))
		raw = q.fetchall()
		if raw:
			uids = [ uid[0] for uid in raw ]
			return uids
		return []