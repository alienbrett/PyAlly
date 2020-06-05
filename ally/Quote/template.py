def template ( cls ):
	
	def x ( self, **kwargs ):
		"""Use self.auth to query for current account holdings
		"""
		result = cls(
			auth = self.auth,
			account_nbr = self.account_nbr,
			**kwargs
		).request()


		if kwargs.get('dataframe',True):
			try:
				result = cls.DataFrame ( result )
			except:
				raise
		

		return result
	
	return x
