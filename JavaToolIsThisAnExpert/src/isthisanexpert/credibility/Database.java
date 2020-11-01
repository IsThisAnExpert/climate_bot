package isthisanexpert.credibility;

import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

import isthisanexpert.credibility.model.CredibilityScore;
import isthisanexpert.credibility.model.Retweet;
import isthisanexpert.credibility.model.Tweet;
import isthisanexpert.credibility.model.User;

public class Database {

	// TODO do db export and commit exported SQL
	
	private static Connection connection = null;
	
	public static Connection getConnectionInstance() {
		return connection;
	}

	public Database()
	{
        try {
        	if( connection == null) {
        		// TODO remove credentials
        		String url = "jdbc:mysql://hostname:3306/hackathon";
                String username = "hackathon";
                String password = "mypassword";
        		connection = DriverManager.getConnection(url, username, password);
        	}
        }
        catch (SQLException e) {
            //JOptionPane.showMessageDialog(null, "Could not connect to database! " 
            //		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        	e.printStackTrace();
        }
	}
	
	public PreparedStatement prepareStatement(String sql) {
		try {
			return connection.prepareStatement(sql);
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not prepare SQL statement! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
		return null;
	}
	
	public User getUser(BigDecimal id) {
		PreparedStatement preparedStatement = prepareStatement(
				"SELECT * FROM hackathon.new_user WHERE id = ?");
    	try {
	    	preparedStatement.setBigDecimal(1, id);
	        ResultSet resultSet = preparedStatement.executeQuery();
	        resultSet.next();
	        User user = new User(resultSet.getBigDecimal("id"));
	        user.setName(resultSet.getString("name"));
	        //user.setTimeCreated(resultSet.getTimestamp("created_at"));
	        // URL
			return user;
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not find user! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
    	return null;
	}
	
	public User getUserByName(String username) {
		PreparedStatement preparedStatement = prepareStatement(
				"SELECT * FROM hackathon.new_user WHERE name LIKE ?");
    	try {
    		System.out.println(username);
	    	preparedStatement.setString(1, username);
	        ResultSet resultSet = preparedStatement.executeQuery();
	        if(resultSet.next()) {
	        	User user = new User(resultSet.getBigDecimal("id"));
	        	user.setName(resultSet.getString("name"));
	        	//user.setTimeCreated(resultSet.getTimestamp("created_at"));
	        	// URL
	        	return user;	        	
	        }
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not find user! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
    	return null;
	}
	
	public void insertCredibilityScore(BigDecimal userId, float score) {
		PreparedStatement preparedStatement = prepareStatement(
				"INSERT INTO hackathon.new_credibility (score, type, user_id, created_at) VALUES (?, 'manual', ?, ?)");
		try {
			preparedStatement.setFloat(1, score);
			preparedStatement.setBigDecimal(2, userId);
			preparedStatement.setTimestamp(3, new Timestamp(System.currentTimeMillis()));
			preparedStatement.executeUpdate();
		} catch(SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not insert credibility score! " 
			//	+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
	}
	
	public CredibilityScore getCredibilityScoreByUser(User user) {
		PreparedStatement preparedStatement = prepareStatement(
				"SELECT * FROM hackathon.new_credibility WHERE user_id LIKE ?");
    	try {
	    	preparedStatement.setBigDecimal(1, user.getId());
	        ResultSet resultSet = preparedStatement.executeQuery();
	        if(resultSet.next()) {
	        	CredibilityScore score = new CredibilityScore(resultSet.getBigDecimal("id"));
	        	score.setScore(resultSet.getFloat("score"));
	        	score.setUser(getUser(resultSet.getBigDecimal("user_id")));
	        	return score;	        	
	        }
	        
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not find score! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
    	return null;
	}
	
	public CredibilityScore getCredibilityScore(BigDecimal id) {
		PreparedStatement preparedStatement = prepareStatement(
				"SELECT * FROM hackathon.new_credibility WHERE id = ?");
    	try {
	    	preparedStatement.setBigDecimal(1, id);
	        ResultSet resultSet = preparedStatement.executeQuery();
	        resultSet.next();
	        
	        CredibilityScore score = new CredibilityScore(id);
	        score.setScore(resultSet.getFloat("score"));
	        score.setUser(getUser(resultSet.getBigDecimal("user_id")));
			return score;
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not find score! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
    	return null;
	}
	
	public List<Retweet> getAllRetweets(User user) {
		ArrayList<Retweet> listOfRetweets = new ArrayList<>();
		PreparedStatement preparedStatement = prepareStatement(
				"SELECT * FROM hackathon.new_retweet WHERE retweeted_by = ?");
    	try {
	    	preparedStatement.setBigDecimal(1, user.getId());
	        ResultSet resultSet = preparedStatement.executeQuery();
	        while(resultSet.next()) {
	        	Retweet retweet = new Retweet(resultSet.getBigDecimal("id"));
		        retweet.setSource(getTweet(resultSet.getBigDecimal("source_tweet_id")));
		        retweet.setUser(user);
		        Tweet tweet = getTweet(resultSet.getBigDecimal("id"));
		        if(tweet != null) {
		        	retweet.setUserScreenName(tweet.getUserScreenName());
		        	retweet.setContent(tweet.getContent());
		        	retweet.setType(tweet.getType());
		        	retweet.setUrl(tweet.getUrl());
		        	// retweet.setTimePosted(
		        	listOfRetweets.add(retweet);
		        }
	        }
			return listOfRetweets;
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not find retweets! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
    	return null;
	}
	
	public List<Retweet> getRetweet(BigDecimal id) {
		PreparedStatement preparedStatement = prepareStatement(
				"SELECT * FROM hackathon.new_retweet WHERE id = ?");
    	try {
	    	preparedStatement.setBigDecimal(1, id);
	        ResultSet resultSet = preparedStatement.executeQuery();
	        resultSet.next();
        	Retweet retweet = new Retweet(id);
	        retweet.setSource(getTweet(resultSet.getBigDecimal("source_tweet_id")));
	        retweet.setUser(getUser(resultSet.getBigDecimal("retweeted_by")));
	        Tweet tweet = getTweet(id);
	        retweet.setUserScreenName(tweet.getUserScreenName());
	        retweet.setContent(tweet.getContent());
	        retweet.setType(tweet.getType());
	        retweet.setUrl(tweet.getUrl());
	        // retweet.setTimePosted(
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not find retweets! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
    	return null;
	}
	
	public List<Tweet> getTweets(User user, boolean skipRetweets) {
		ArrayList<Tweet> listOfTweets = new ArrayList<>();
		String sql = "SELECT * FROM hackathon.new_tweet WHERE user_id = ?";
		if(skipRetweets) {
			sql = "SELECT * FROM hackathon.new_tweet WHERE user_id = ? AND type = 0";
		}
		PreparedStatement preparedStatement = prepareStatement(sql);
    	try {
	    	preparedStatement.setBigDecimal(1, user.getId());
	        ResultSet resultSet = preparedStatement.executeQuery();
	        while(resultSet.next()) {
	        	Tweet tweet = new Tweet(resultSet.getBigDecimal("id"));
		        tweet.setUser(user);
		        tweet.setUserScreenName(resultSet.getString("user_screen_name"));
		        tweet.setContent(resultSet.getString("content"));
		        tweet.setType(resultSet.getString("type"));
		        tweet.setUrl(resultSet.getString("type"));
		        // tweet.setTimePosted(resultSet.getTimestamp("posted_time"));
		        listOfTweets.add(tweet);
	        }
			return listOfTweets;
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not find tweets! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
    	return null;
	}
	
	public Tweet getTweet(BigDecimal id) {
		PreparedStatement preparedStatement = prepareStatement(
				"SELECT * FROM hackathon.new_tweet WHERE id = ?");
    	try {
	    	preparedStatement.setBigDecimal(1, id);
	        ResultSet resultSet = preparedStatement.executeQuery();
	        if(resultSet.next()) {
	        	Tweet tweet = new Tweet(id);
	        	tweet.setUser(getUser(resultSet.getBigDecimal("user_id")));
	        	tweet.setUserScreenName(resultSet.getString("user_screen_name"));
	        	tweet.setContent(resultSet.getString("content"));
	        	tweet.setType(resultSet.getString("type"));
	        	tweet.setUrl(resultSet.getString("type"));
	        	// tweet.setTimePosted(resultSet.getTimestamp("posted_time"));
	        	return tweet;
	        }
	        
		} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not find tweets! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
    	return null;
	}
	
	public CredibilityScore findCredibilityScoreForUser(User user) {
		PreparedStatement preparedStatement = prepareStatement(
				"SELECT * FROM hackathon.new_credibility WHERE user_id = ?");
    	try {
	    	preparedStatement.setBigDecimal(1, user.getId());
	        ResultSet resultSet = preparedStatement.executeQuery();
	        if(resultSet.next()) {
	        	CredibilityScore score = new CredibilityScore(resultSet.getBigDecimal("id"));
	        	score.setScore(resultSet.getFloat("score"));
		        score.setUser(user);
	        } else {
	        	return null;
	        }
    	} catch (SQLException e) {
			//JOptionPane.showMessageDialog(null, "Could not search scores! " 
			//		+ e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
    		e.printStackTrace();
		}
    	return null;
	}
	
	@Override
	protected void finalize() throws Throwable {
		super.finalize();
		if(connection != null) {
			/*
        	try {
				connection.close();
			} catch (SQLException e) {
				// ignore
			}
			*/
        }
	}
}
