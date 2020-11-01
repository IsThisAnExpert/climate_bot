package isthisanexpert.credibility.listener;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JTextField;

import isthisanexpert.credibility.CredibiltyScoreProcessor;

public class CalculateScoreActionListener implements ActionListener {
	private JTextField txtUsername;

	public CalculateScoreActionListener(JTextField txtUsername) {
		super();
		this.txtUsername = txtUsername;
	}

	@Override
	public void actionPerformed(ActionEvent event) {
		CredibiltyScoreProcessor scoreProcessor = new CredibiltyScoreProcessor();
		scoreProcessor.process(txtUsername.getText());
	}
}
