package isthisanexpert.credibility;

import java.awt.GridLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;

import isthisanexpert.credibility.listener.AssignScoreActionListener;
import isthisanexpert.credibility.listener.CalculateScoreActionListener;

public class IsThisAnExpertFrame extends JFrame implements Runnable {

	private static final long serialVersionUID = 4625980564070704383L;

	public IsThisAnExpertFrame() {
		super("IsThisAnExpert - Tool for assigning a credibility score");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 600, 200);
		GridLayout layout = new GridLayout(0,2);
		setLayout(layout);
	}

	@Override
	public void run() {
		JLabel lblUsername = new JLabel("Username: ");
		JTextField txtUsername = new JTextField();
		
		JLabel lblScore = new JLabel("Credibility score: ");
		JTextField txtScore = new JTextField("0");
		
		JButton butAssignScore = new JButton("Assign credibility score to twitter user");
		butAssignScore.addActionListener(new AssignScoreActionListener(txtUsername, txtScore));
		
		add(lblUsername);
		add(txtUsername);
		add(lblScore);
		add(txtScore);
		add(butAssignScore);
		
		// make space :-)
		add(new JLabel());
		add(new JLabel());
		add(new JLabel());
		
		JLabel lblUsername2 = new JLabel("Username: ");
		JTextField txtUsername2 = new JTextField();
		
		JButton butCalculateScore = new JButton("Calculate credibility score for twitter user");
		butCalculateScore.addActionListener(new CalculateScoreActionListener(txtUsername2));
		
		add(lblUsername2);
		add(txtUsername2);
		add(butCalculateScore);
		
		setVisible(true);
	}
}
