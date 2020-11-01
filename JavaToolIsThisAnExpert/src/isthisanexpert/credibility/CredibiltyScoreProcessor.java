package isthisanexpert.credibility;

import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

import isthisanexpert.credibility.model.CredibilityScore;
import isthisanexpert.credibility.model.Retweet;
import isthisanexpert.credibility.model.Tweet;
import isthisanexpert.credibility.model.User;

public class CredibiltyScoreProcessor {

	/**
	 * computes a credibility score for a twitter user 
	   based on the credibility scores of their sources and their references.
	   (possible extension: add one more layer of breadth-first-search to look for credible sources.)
	 * @param username a user to be examined 
	 * @return a credibility score for that user
	 */
	public float calculateScore(User user) {
	    Database db = new Database();
		
	    // link_counter counts the number of tweets + retweets that the user published
	    // it is a measure for activity of the user
	    int linkCounter = 0;
	    float discountFactor = 0.1f;
	    float scoreValue = 0;

	    for(Retweet retweet: db.getAllRetweets(user)) {
	    	linkCounter += 1;
	        //if user that is referenced is credible, 
	        //the user that references them is probably also credible.

	    	// TODO import more data into db
	    	if(retweet.getSource() != null) {
	    		User originalUser = retweet.getSource().getUser();
	    		CredibilityScore originalUserScore = db.getCredibilityScoreByUser(originalUser);
	    		if(isCredible(originalUser, originalUserScore)) { 
	    			scoreValue += originalUserScore.getScore();
	    		}
	    		// TODO evaluate also retweet sources from original user
	    	}
	    }
	    for(Tweet tweet: db.getTweets(user, true)) {
	    	linkCounter += 1;
	    	// if user that is referenced is credible, 
	        // the user that references them is probably also credible.
	    	for(User referencedUser: getReferencedUsers(tweet)) {
	    		CredibilityScore referencedUserScore = db.getCredibilityScoreByUser(referencedUser); 
	    		if(isCredible(referencedUser, referencedUserScore))
		    	{
		    		scoreValue += referencedUserScore.getScore();
		    	}
	    	}
	    	
	    }
	    
	    // TODO check credibility of linked websites?
	    
	    // multiply by 0 < discount_factor < 1
	    // assure that users that reference have lower credibility scores than the users they reference
	    scoreValue = scoreValue * discountFactor;
	    // relate the score to the activity of the user 
	    // (i. e. ratio of relevant topics is computed rather than an absolute value)
	    if(linkCounter > 0)
	    {
	    	scoreValue = scoreValue / linkCounter;
	    }
	    
	    // tanh(x) to hold values within a reasonable range
	    scoreValue = (float) Math.tanh(scoreValue);

	    return scoreValue;
	}
	
	private boolean isCredible(User user, CredibilityScore score) {
		return score != null && (score.getScore() > 3 || score.getScore() < -3);
	}
	
	/**
	 * looks for user mentionings in tweet content, e.g. @JohnDoe
	 * @param tweet parsed tweet
	 * @return referenced users in tweet
	 */
	private List<User> getReferencedUsers(Tweet tweet) {
		Database db = new Database();
		ArrayList<User> listOfUsers = new ArrayList<>();
		// parse tweet for @username where username is in db user table
		StringTokenizer tokenizer = new StringTokenizer("dummyvalue"+tweet.getContent(), "@ ");
		while(tokenizer.hasMoreTokens()) {
			String token = tokenizer.nextToken("@");
			if( tokenizer.hasMoreTokens()) {
				token = tokenizer.nextToken(" ");
			}
			String username = token;
			User reference = db.getUserByName(username);
			if(reference != null) {
				listOfUsers.add(reference);
			}
		}
		return listOfUsers;
	}
	
	public void process(String username) {
		Database db = new Database();
        User user = db.getUserByName(username);
        CredibilityScore score = db.findCredibilityScoreForUser(user);
        // no score in database found for this user
        if(score == null) {
        	db.insertCredibilityScore(user.getId(), calculateScore(user));
        }
	}

}
