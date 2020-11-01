package isthisanexpert.credibility.model;

import java.math.BigDecimal;

public class CredibilityScore {
	private BigDecimal id;
	private float score;
	private User user;

	public CredibilityScore(BigDecimal id) {
		this.id = id;
	}

	public BigDecimal getId() {
		return id;
	}
	
	public float getScore() {
		return score;
	}

	public void setScore(float score) {
		this.score = score;
	}

	public User getUser() {
		return user;
	}

	public void setUser(User user) {
		this.user = user;
	}
}
