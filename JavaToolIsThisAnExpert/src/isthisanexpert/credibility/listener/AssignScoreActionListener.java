package isthisanexpert.credibility.listener;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JTextField;

import isthisanexpert.credibility.Database;
import isthisanexpert.credibility.model.User;

public class AssignScoreActionListener implements ActionListener {
	private JTextField txtUsername;
	private JTextField txtCredibilityScore;

	public AssignScoreActionListener(JTextField txtUsername, JTextField txtCredibilityScore) {
		super();
		this.txtUsername = txtUsername;
		this.txtCredibilityScore = txtCredibilityScore;
	}

	@Override
	public void actionPerformed(ActionEvent event) {
		Database db = new Database();
        User user = db.getUserByName(txtUsername.getText());
        db.insertCredibilityScore(user.getId(), Float.parseFloat(txtCredibilityScore.getText()));
	}
}
