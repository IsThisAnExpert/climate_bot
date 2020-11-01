package isthisanexpert.credibility;

/***
 * This code is part of the IsThisAnExpert project for the climate hackathon 2020
 *
 */
public class Main {
	public static void main( String[] args)
	{
		if(args.length == 2 && "--calculate-score".equals(args[0]))
		{
			// called by command line by our twitter bot
			String username = args[1];
			CredibiltyScoreProcessor scoreProcessor = new CredibiltyScoreProcessor();
			scoreProcessor.process(username);
		} else {
			new IsThisAnExpertFrame().run();
		}
	}
}
