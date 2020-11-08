CREATE TABLE `new_credibility` (
  `id` bigint(42) NOT NULL,
  `score` float NOT NULL,
  `type` varchar(255) NOT NULL COMMENT 'manually chosen or calculated',
  `user_id` bigint(42) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `new_retweet` (
  `id` bigint(42) NOT NULL,
  `tweet_id` bigint(42) NOT NULL,
  `retweeted_by` bigint(42) NOT NULL,
  `source_tweet_id` bigint(42) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `new_tweet` (
  `id` bigint(42) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `posted_time` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL COMMENT '0: normal, 1:retweet',
  `user_screen_name` varchar(42) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `new_user` (
  `id` bigint(42) NOT NULL,
  `name` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `created_time` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
