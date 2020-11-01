package isthisanexpert.credibility.model;

import java.math.BigDecimal;
import java.sql.Timestamp;

public class Tweet {
	private BigDecimal id;
	private String content;
	private User user;
	private Timestamp timePosted;
	private String url;
	private String type;
	// TODO transfer screenName to User?
	private String userScreenName;
	
	public Tweet(BigDecimal id)
	{
		this.id = id;
	}
	
	public BigDecimal getId() {
		return id;
	}
	
	public String getContent() {
		return content;
	}
	
	public void setContent(String content) {
		this.content = content;
	}
	
	public User getUser() {
		return user;
	}
	
	public void setUser(User user) {
		this.user = user;
	}
	
	public Timestamp getTimePosted() {
		return timePosted;
	}
	
	public void setTimePosted(Timestamp timePosted) {
		this.timePosted = timePosted;
	}
	
	public String getUrl() {
		return url;
	}
	
	public void setUrl(String url) {
		this.url = url;
	}
	
	public String getType() {
		return type;
	}
	
	public void setType(String type) {
		this.type = type;
	}
	
	public String getUserScreenName() {
		return userScreenName;
	}
	
	public void setUserScreenName(String userScreenName) {
		this.userScreenName = userScreenName;
	}
}
