public static void main(String[] args) throws IOException {
		List<NameValuePair> params = new LinkedList<>();
		params.add(new BasicNameValuePair("email", "531575027@qq.com"));
		params.add(new BasicNameValuePair("pass", "*********"));
		params.add(new BasicNameValuePair("remember", "on"));

		String loginUrl = "https://www.tudouvpn.com/login.php";
		String dailyUrl = "https://www.tudouvpn.com/daily.php";

		CloseableHttpClient client = HttpClients.createDefault();
		try {
			RequestConfig config = RequestConfig.custom().setConnectTimeout(10000).setSocketTimeout(10000).build();
			HttpClientBuilder clientBuilder = HttpClientBuilder.create();
			CookieStore cookie = new BasicCookieStore();
			clientBuilder.setDefaultCookieStore(cookie);
			client = clientBuilder.build();

			HttpPost post = new HttpPost(loginUrl);
			post.setHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8");
			post.setHeader("Upgrade-Insecure-Requests", "1");
			post.setHeader("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36");
			post.setHeader("Referer", "https://www.tudouvpn.com/login.php");
			post.setHeader("Accept-Encoding", "gzip, deflate, sdch");
			post.setHeader("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2");
			post.setConfig(config);
			post.setEntity(new UrlEncodedFormEntity(params));


			HttpResponse response = client.execute(post);
			int statusCode = response.getStatusLine().getStatusCode();
			for (Cookie entry : cookie.getCookies()) {
				System.out.println(entry.getName());
				System.out.println(entry.getValue());
			}

			HttpGet get = new HttpGet(dailyUrl);
			get.setHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8");
			get.setHeader("Upgrade-Insecure-Requests", "1");
			get.setHeader("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36");
			get.setHeader("Referer", "https://www.tudouvpn.com/login.php");
			get.setHeader("Accept-Encoding", "gzip, deflate, sdch");
			get.setHeader("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2");
//			get.setHeader("Cookie", "u2=e392270045c0071bfb1ac6b7f7c79be8");
			get.setConfig(config);

			response = client.execute(get);
			statusCode = response.getStatusLine().getStatusCode();
			System.out.println(statusCode);

			System.out.println(EntityUtils.toString(response.getEntity()));

		} finally {
			try {client.close();} catch (IOException e) {}
		}
	}
}