package isthisanexpert.credibility.model;

import java.math.BigDecimal;

public class Retweet extends Tweet {
	private Tweet source;
	
	public Retweet(BigDecimal id) {
		super(id);
	}
	
	public Tweet getSource() {
		return source;
	}
	
	public void setSource(Tweet source) {
		this.source = source;
	}
}
