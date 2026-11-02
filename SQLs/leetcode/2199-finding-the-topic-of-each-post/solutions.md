# 2199. Finding the Topic of Each Post - Solutions

## Solution 1: Whole-word match via padded `INSTR`

A naive substring check (`content LIKE '%war%'`) would wrongly match "war" inside "warning". Padding both `content` and `word` with a leading/trailing space turns the search into a whole-word test: `' warning '` never contains `' war '`, but `' stop the war and play handball '` does contain `' war '`.

`LEFT JOIN` keeps posts that match no keyword at all, and `GROUP_CONCAT(DISTINCT topic_id)` collapses all matching topics (deduplicated, sorted ascending by default) into the comma-separated string the problem asks for. `COALESCE` swaps in `'Ambiguous!'` when a post produced no matches (an all-`NULL` group from the left join).

#### MySQL

```sql
SELECT
    p.post_id,
    COALESCE(GROUP_CONCAT(DISTINCT k.topic_id ORDER BY k.topic_id), 'Ambiguous!') AS topic
FROM Posts p
LEFT JOIN Keywords k
    ON INSTR(CONCAT(' ', p.content, ' '), CONCAT(' ', k.word, ' ')) > 0
GROUP BY p.post_id;
```
With Regexp
``` sql
select 
	p.post_id, 
	GROUP_CONCAT( 
	distinct coalesce(k.topic_id, 'Ambiguous!') 
	order by k.topic_id 
	separator ',') AS topic -- separator ',' is optioanl as , is default
from 
	Posts p
	left join Keywords k
on content regexp concat('\\b', k.word, '\\b')
group by 1 order by 1;
```
