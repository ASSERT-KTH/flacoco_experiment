## INRIA/Spoon

### PR 4704
- Date: 22 April 2022
- Status: closed without merging it
- Details: [Link](https://github.com/INRIA/spoon/pull/4704)

Failed tests:
- TestSniperPrinter.testNoChangeDiff(File)[1] Method testNoChangeDiff must fail (more details [here](https://github.com/INRIA/spoon/runs/6126325689?check_suite_focus=true))

The lines found by flacocobot are not contained in the diff and they are associated with failed tests that are not the same of the ones detected on GitHub CI.

### PR 4709
- Date: 24 April 2022
- Status: Open
- Details: [Link](https://github.com/INRIA/spoon/pull/4709)

Failed tests:
- JavaReflectionTreeBuilderTest.testInnerClass:657 expected: `<true>` but was: `<false>`

Details about the lines found by Flacocobot:
- Flacocobot found 4 suspicious lines matching the diff and it left [a comment to the PR](https://github.com/INRIA/spoon/pull/4709#pullrequestreview-951192304);
- The lines associated with failed tests are not the same of the ones detected on GitHub CI;
- Two developers reacted to the comment with the "confused" emoji :confused:;
- The lines matching the diff have lower suspiciousness score (5.75% and 0.92%) than the lines that are not contained in the diff (92.53% and 92.48%).

### Other details

For both the pull requests, Flacocobot found the same suspicious lines.

### PR 4748
- Date: 13 June 2022
- Status: Open
- Details: [Link](https://github.com/INRIA/spoon/pull/4748)

#### 16:47 CEST

Failed tests (Tests with Java 17 on ubuntu-latest)
- Error: spoon.test.architecture.SpoonArchitectureEnforcerTest.testSpecPackage  Time elapsed: 4.309 s  <<< FAILURE!202
java.lang.AssertionError: you have created a new package or removed an existing one, please declare it explicitly in SpoonArchitectureEnforcerTest#testSpecPackage
- SpoonArchitectureEnforcerTest.testSpecPackage:448->assertSetEquals:457 you have created a new package or removed an existing one, please declare it explicitly in SpoonArchitectureEnforcerTest#testSpecPackage

Other failures related to extra checks (missing licence header) and code quality qodana.

The lines found by flacocobot are not contained in the diff. Differences in failed tests between flacocobot and CI. There are more failed tests according flacocobot.

#### 16:49 CEST

Failed tests (Tests with Java 11 on ubuntu-latest)
- Error: SpoonArchitectureEnforcerTest.testSrcMainJava:201 2 public methods should be documented with proper API documentation: spoon.javadoc.external.parsing.StringReader#readBalancedBraced()
spoon.javadoc.external.parsing.StringReader#readPotentiallyQuoted()

Other failures related extra checks (Javadoc quality has deteriorated!) and code quality qodana.

The lines found by flacocobot are not contained in the diff. Differences in failed tests between flacocobot and CI. The failed test in CI is not failed with flacocobot.

### PR 4751
- Date: 20 June 2022
- Status: Open
- Details: [Link](https://github.com/INRIA/spoon/pull/4751)

Tests run: 1720, Failures: 15, Errors: 23, Skipped: 13 (Tests with Java 11 on windows-latest)
Tests run: 1720, Failures: 16, Errors: 23, Skipped: 11 (Tests with Java 17 on ubuntu-latest)

Other failures related extra checks (checkstyle errrors) and code quality qodana.

Flacocobot found 5 suspicious lines matching the diff. Not all the failed tests on CI are failed with Flacocobot. Moreover, there are more failed tests detected by Flacocobot. Flacocobot comment has been ignored by developers. Flacocobot reports also lines related to test cases.

## Apache Dubbo

### PR 9893
- Date: 3 April 2022
- Status: closed without merging it
- Details: [Link](https://github.com/apache/dubbo/pull/9893)

Failed tests:
- StickyTest.testMethodStickyNoCheck:93 expected: `<true>` but was: `<false>`

The lines found by flacocobot are not contained in the diff and they are associated with failed tests that are not the same of the ones detected on GitHub CI.

## Apache Shardingsphere

### PRs discarded by the analysis:
- [#16609](https://github.com/apache/shardingsphere/pull/16609) because the changes are related to .MD files - [Link](https://github.com/apache/shardingsphere/pull/16609/files)
- [#17251](https://github.com/apache/shardingsphere/pull/17251) because the failures are related also to style rules (e.g., build fails due to WhitespaceAround: 'for' is not followed by whitespace.) - [Link](https://github.com/apache/shardingsphere/runs/6245792624?check_suite_focus=true)


### PR 16952 (Maybe to discard)
- Date: 20 April 2022
- Status: Merged
- Details: [Link](https://github.com/apache/shardingsphere/pull/16952)
- Other information: 61 changed files, the next changes introduce fix in the test cases

Failed tests [Link](https://github.com/apache/shardingsphere/runs/6091634813?check_suite_focus=true):
- assertBuildOfAllShardingTables(org.apache.shardingsphere.infra.metadata.schema.builder.SchemaBuilderTest) - java.lang.AssertionError: Expected: is `<1>` but: was `<0>` at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:20)
- assertLoadWithExistedTableName(org.apache.shardingsphere.infra.metadata.schema.builder.TableMetaDataBuilderTest) - java.lang.AssertionError
- assertLoadWithoutTables(org.apache.shardingsphere.infra.metadata.schema.loader.dialect.PostgreSQLTableMetaDataLoaderTest) - java.lang.AssertionError: Expected: is `<1>` but: was `<0>` at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:20)
- assertLoadWithTables(org.apache.shardingsphere.infra.metadata.schema.loader.dialect.PostgreSQLTableMetaDataLoaderTest) - java.lang.AssertionError: Expected: is `<1>`but: was `<0>` at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:20)
- SchemaBuilderTest.assertBuildOfAllShardingTables:65 Expected: is `<1>` but: was `<0>`
- TableMetaDataBuilderTest.assertLoadWithExistedTableName:52
- PostgreSQLTableMetaDataLoaderTest.assertLoadWithTables:88->assertTableMetaDataMap:148 Expected: is `<1>` but: was `<0>`
- PostgreSQLTableMetaDataLoaderTest.assertLoadWithoutTables:74->assertTableMetaDataMap:148 Expected: is `<1>` but: was `<0>`

The lines found by flacocobot are not contained in the diff and they are associated with failed tests that are not the same of the ones detected on GitHub CI.

### PR 17047 (Maybe to discard)
- Date: 24 April 2022
- Status: Merged
- Details: [Link](https://github.com/apache/shardingsphere/pull/17047)
- Other information: 37 changed files, the next changes introduce fix in the test cases

Failed tests:
- assertDecorateForRouteContextWhenIsFederated(org.apache.shardingsphere.sharding.rewrite.context.ShardingSQLRewriteContextDecoratorTest) - java.lang.AssertionError at org.apache.shardingsphere.sharding.rewrite.context.ShardingSQLRewriteContextDecoratorTest.assertDecorateForRouteContextWhenIsFederated(ShardingSQLRewriteContextDecoratorTest.java:48)
- ShardingSQLRewriteContextDecoratorTest.assertDecorateForRouteContextWhenIsFederated:48

The lines found by flacocobot are not contained in the diff and they are associated with failed tests that are not the same of the ones detected on GitHub CI.

### PR 17110 (Maybe to discard)
- Date: 26 April 2022
- Status: Merged
- Details: [Link](https://github.com/apache/shardingsphere/pull/17110)
- Other information: 42 changed files, the next changes introduce fix in the test cases

Tests failed [Link](https://github.com/apache/shardingsphere/runs/6169003863?check_suite_focus=true)
- Tests run: 364, Failures: 0, Errors: 32, Skipped: 0

The lines found by flacocobot are not contained in the diff.

### PR 17122 (Maybe to discard)
- Date: 26 April 2022
- Status: Merged
- Details: [Link](https://github.com/apache/shardingsphere/pull/17122)
- Other information: 35 changed files, the next changes introduce fix in the test cases and for the checkstyle

Failed tests:
- assertGenerateSQLTokens(org.apache.shardingsphere.sharding.rewrite.token.IndexTokenGeneratorTest)
- IndexTokenGeneratorTest.assertGenerateSQLTokens:68 NullPointer Cannot invoke "...

The lines found by flacocobot are not contained in the diff and they are associated with failed tests that are not the same of the ones detected on GitHub CI.

### PR 17174 (Maybe to discard)
- Date: 28 April 2022
- Status: Merged
- Details: [Link](https://github.com/apache/shardingsphere/pull/17174)
- Other information: 64 changed files, the next changes introduce fix in the test cases the in the checkstyle

Failed tests:
- Tests run: 802, Failures: 0, Errors: 20, Skipped: 0 [Link](https://github.com/apache/shardingsphere/runs/6209061538?check_suite_focus=true)

The lines found by flacocobot are not contained in the diff.

### PR 17248 (Maybe to discard)
- Date: 1 May 2022
- Status: Merged
- Details: [Link](https://github.com/apache/shardingsphere/pull/17248)
- Other information: 6 changed files, the next changes introduce fix in the test cases

Failed tests:
- org.apache.shardingsphere.proxy.backend.text.distsql.ral.common.updatable.AlterSQLParserRuleHandlerTest
- assertExecuteWithoutCurrentRuleConfiguration(org.apache.shardingsphere.proxy.backend.text.distsql.ral.common.updatable.AlterSQLParserRuleHandlerTest) 
- assertExecuteWithDefaultRuleConfiguration(org.apache.shardingsphere.proxy.backend.text.distsql.ral.common.updatable.AlterSQLParserRuleHandlerTest)
- AlterSQLParserRuleHandlerTest.assertExecuteWithDefaultRuleConfiguration:72 » ClassCast
- AlterSQLParserRuleHandlerTest.assertExecuteWithoutCurrentRuleConfiguration:51 » ClassCast

The lines found by flacocobot are not contained in the diff and they are associated with failed tests that are not the same of the ones detected on GitHub CI.

### Other details

- For three pull requests ([17047](https://github.com/flacocobot/2022-flacocobot-experiment/blob/main/apache/shardingsphere/17047/2022-04-24T07:13:31.850737Z.md), [17122](https://github.com/flacocobot/2022-flacocobot-experiment/blob/main/apache/shardingsphere/17122/2022-04-26T11:41:54.593381Z.md) and [17174](https://github.com/flacocobot/2022-flacocobot-experiment/blob/main/apache/shardingsphere/17174/2022-04-28T10:44:53.282168Z.md)), Flacocobot found the same suspicious lines.
- For two pull requests ([16952](https://github.com/flacocobot/2022-flacocobot-experiment/blob/main/apache/shardingsphere/16952/2022-04-20T09:34:45.803840Z.md) and [17110](https://github.com/flacocobot/2022-flacocobot-experiment/blob/main/apache/shardingsphere/17110/2022-04-26T03:52:18.943167Z.md)), Flacocobot found the same suspicious lines.

## Debezium

### PR 3382
- Date: 7 April 2022
- Status: Draft
- Details: [Link](https://github.com/debezium/debezium/pull/3382)
- Other information: 19 changed files

Failed tests:
- Information not found

The lines found by flacocobot are not contained in the diff.

### PR 3346 (Maybe to discard)
- Date: 29 April 2022
- Status: Open
- Details: [Link](https://github.com/debezium/debezium/pull/3446)
- Other information: 8 changed files, the next changes introduce fix in the test cases

Failed tests:
- Information not found

The lines found by flacocobot are not contained in the diff.

## Vert.x JDBC client

### PR 273
- Date: 22 March 2022
- Status: Draft
- Details: [Link](https://github.com/vert-x3/vertx-jdbc-client/pull/273)
- Other information: 12 changed files

Failed tests:
- PostgresTest.lambda$setup$0:64 » ContainerLaunch Container startup failed
- *Reading the log file, there are exceptions like java.sql.SQLTransientConnectionException: java.net.UnknownHostException: zoom.zoom.zen.tld*

The lines found by flacocobot are not contained in the diff and they are associated with failed tests that are not the same of the ones detected on GitHub CI.

## Vert.x Web

### PR 2157
- Date: 29 March 2022
- Status: Open
- Details: [Link](https://github.com/vert-x3/vertx-web/pull/2157)
- Other information: 3 changed files

Failed tests:
- Tests run: 183, Failures: 0, Errors: 20, Skipped: 0

The lines found by flacocobot are not contained in the diff.

## Protocol to select Pull Requests to analyze

- Consider pull requests which failure is related to test cases and not to other aspects (e.g., checkstyle errors);
- Discard pull request which changes are not related to Java files;
- Consider pull requests for which flacocobot found suspicious lines;
- Discard pull requests that introduce changes in the test cases to fix the failure?
