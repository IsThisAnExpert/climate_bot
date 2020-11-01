package isthisanexpert.credibility.model;

import java.math.BigDecimal;
import java.sql.Timestamp;

public class User {
	private BigDecimal id;
	private String name;
	private String url;
	private Timestamp timeCreated;

	public User(BigDecimal id) {
		this.id = id;
	}
	
	public BigDecimal getId() {
		return id;
	}
	
	public String getName() {
		return name;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	
	public String getUrl() {
		return url;
	}
	
	public void setUrl(String url) {
		this.url = url;
	}
	
	public Timestamp getTimeCreated() {
		return timeCreated;
	}
	
	public void setTimeCreated(Timestamp timeCreated) {
		this.timeCreated = timeCreated;
	}
}
