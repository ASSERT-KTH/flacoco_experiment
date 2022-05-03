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

Failed tests
- JavaReflectionTreeBuilderTest.testInnerClass:657 expected: `<true>` but was: `<false>`

Flacocobot found suspicious 4 lines matching the diff and it left [a comment to the PR](https://github.com/INRIA/spoon/pull/4709#pullrequestreview-951192304).
The lines are associated with failed tests that are not the same of the ones detected on GitHub CI.
Two developers reacted to the comment with the "confused" emoji `:confused:`

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
- Other information: 61 changed files

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
- Other information: 37 changed files

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
- Other information: 35 changed files, the next changes introduce fix in the test cases the in the checkstyle

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