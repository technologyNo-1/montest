#!/usr/bin/env node
/**
 * parse-exam.js — Parse exam markdown files into structured JSON
 *
 * Input:  exam.md (questions) + answers.md (answers)
 * Output: exam-data.json with CH (choice), SH (short answer), CD (coding) arrays
 *
 * Usage: node parse-exam.js <exam.md> <answers.md> [output.json]
 */

const fs = require('fs');
const path = require('path');

function parseExam(examPath, answersPath) {
  const examRaw = fs.readFileSync(examPath, 'utf8');
  const answersRaw = fs.existsSync(answersPath) ? fs.readFileSync(answersPath, 'utf8') : '';

  const examLines = examRaw.split('\n');
  const answers = parseAnswers(answersRaw);

  const CH = []; // choice
  const SH = []; // short answer
  const CD = []; // coding

  let i = 0;
  let qNum = 0;

  function peek() { return i < examLines.length ? examLines[i] : null; }
  function next() { return i < examLines.length ? examLines[i++] : null; }
  function trim(s) { return s ? s.trim() : ''; }

  // Skip header/title lines
  while (i < examLines.length) {
    const line = trim(peek());
    if (!line || line.startsWith('#') || line.startsWith('（') || line.startsWith('(') ||
        line.match(/^[-=]{3,}$/) || line.match(/^作者/)) {
      i++;
      continue;
    }
    break;
  }

  while (i < examLines.length) {
    const line = trim(peek());
    if (!line) { i++; continue; }

    // Detect section headers
    if (line.match(/^#{1,3}\s*(一|二|三|四|五|六|七|八|九|十|1|2|3|4|5|6|7|8|9|10|选择题|简答题|编程题|问答题|判断题)/)) {
      i++;
      continue;
    }

    // Skip horizontal rules
    if (line.match(/^[-=]{3,}$/)) { i++; continue; }

    // Detect numbered question: "1." or "1、" or "1 ."
    const qMatch = line.match(/^(\d+)\s*[.、．)）]\s*(.+)/);
    if (qMatch) {
      const num = parseInt(qMatch[1]);
      const restOfLine = qMatch[2];

      i++;
      // Collect ALL content until next numbered question or section header
      // (blank lines are OK — options often separated by blank lines)
      let qBody = restOfLine;
      let blankStreak = 0;
      while (i < examLines.length) {
        const nl = peek();
        const nlTrim = trim(nl);

        // Stop only at next numbered question or section header
        if (nlTrim.match(/^\d+\s*[.、．)）]\s/)) break;
        if (nlTrim.match(/^#{1,3}\s/)) break;

        // Track blank lines — allow gaps between code block and options
        if (!nlTrim) {
          blankStreak++;
          // Look ahead further: is there a non-blank line that's part of this question?
          let foundContent = false;
          for (let k = i + 1; k < Math.min(i + 10, examLines.length); k++) {
            const ahead = trim(examLines[k]);
            if (!ahead) continue;
            if (ahead.match(/^\d+\s*[.、．)）]/) || ahead.match(/^#{1,3}\s/)) break;
            foundContent = true;
            break;
          }
          if (!foundContent && blankStreak > 10) { i++; break; }
          i++; continue; // skip blanks but keep looking for options
        } else {
          blankStreak = 0;
        }

        // Collect code blocks fully (markdown ``` or HTML <pre><code>)
        if (nlTrim.startsWith('```') || nlTrim.includes('<pre><code>')) {
          if (nlTrim.startsWith('```')) {
            let codeBlock = '';
            i++; // skip opening ```
            while (i < examLines.length) {
              const cl = next();
              if (trim(cl).startsWith('```')) break;
              codeBlock += (codeBlock ? '\n' : '') + cl;
            }
            qBody += '\n```' + codeBlock + '```';
          } else {
            // HTML <pre><code> block — collect until </code></pre>
            let htmlBlock = nlTrim;
            i++;
            while (i < examLines.length) {
              const cl = next();
              htmlBlock += '\n' + cl;
              if (cl.includes('</code>') || cl.includes('</pre>')) break;
            }
            qBody += '\n' + htmlBlock;
          }
          continue;
        }
        qBody += '\n' + nlTrim;
        i++;
      }

      // Detect question type
      const hasCodeBlock = qBody.includes('```') || qBody.includes('<pre><code>');
      // Detect options: A./A、 with optional blank lines between them
      const hasOptions = /\n\s*[A-D]\s*[.、．)）]\s*/.test(qBody) ||
                         /^[A-D]\s*[.、．)）]\s*/.test(qBody) ||
                         (qBody.match(/[A-D]\s*[.、．)）][^\n]*\n\s*\n\s*[A-D]\s*[.、．)）]/));

      // Choice questions take priority if they have BOTH options AND code (code in question stem)
      if (hasOptions && hasCodeBlock) {
        // Could be choice-with-code OR coding — check for options AFTER code block
        // Handle both ``` and <pre><code> endings
        let codeEnd = qBody.lastIndexOf('```');
        if (codeEnd < 0) codeEnd = qBody.lastIndexOf('</pre>');
        if (codeEnd < 0) codeEnd = qBody.lastIndexOf('</code>');
        const afterCode = codeEnd >= 0 ? qBody.substring(codeEnd) : '';
        const hasOptionsAfterCode = /\n\s*[A-D]\s*[.、．)）]\s*/.test(afterCode);
        if (hasOptionsAfterCode) {
          // Definitely choice question with code in stem
          const parsed = parseChoiceQuestion(qBody);
          CH.push({
            id: CH.length + 1,
            num: num,
            q: parsed.stem,
            o: parsed.options,
            a: parsed.correctIndex !== null ? parsed.correctIndex : 0,
            e: (answers[num] && answers[num].explanation) || ''
          });
        } else {
          // Code question (coding problem)
          const parsed = parseCodingQuestion(qBody);
          const ans = answers[num] || {};
          CD.push({
            id: CD.length + 1,
            num: num,
            q: parsed.stem,
            s: parsed.starter || '',
            a: ans.code || ans.fullAnswer || '',
            t: ans.testCases || []
          });
        }
      } else if (hasOptions && !hasCodeBlock) {
        // ===== CHOICE QUESTION =====
        const parsed = parseChoiceQuestion(qBody);
        CH.push({
          id: CH.length + 1,
          num: num,
          q: parsed.stem,
          o: parsed.options,
          a: parsed.correctIndex !== null ? parsed.correctIndex : 0,
          e: (answers[num] && answers[num].explanation) || ''
        });
      } else if (hasCodeBlock || qBody.match(/编写|实现|写一个|定义.*函数|def\s+\w+/)) {
        // ===== CODING QUESTION =====
        const parsed = parseCodingQuestion(qBody);
        const ans = answers[num] || {};
        CD.push({
          id: CD.length + 1,
          num: num,
          q: parsed.stem,
          s: parsed.starter || '',
          a: ans.code || ans.fullAnswer || '',
          t: ans.testCases || []
        });
      } else {
        // ===== SHORT ANSWER QUESTION =====
        SH.push({
          id: SH.length + 1,
          num: num,
          q: qBody.replace(/\n/g, ' ').trim(),
          a: (answers[num] && answers[num].htmlAnswer) || ''
        });
      }
      continue;
    }

    // Skip unrecognized lines
    i++;
  }

  // Re-number IDs
  CH.forEach((q, i) => q.id = i + 1);
  SH.forEach((q, i) => q.id = i + 1);
  CD.forEach((q, i) => q.id = i + 1);

  return { CH, SH, CD, meta: {
    title: extractTitle(examRaw),
    choiceCount: CH.length,
    shortCount: SH.length,
    codeCount: CD.length,
    total: CH.length + SH.length + CD.length
  }};
}

function parseChoiceQuestion(body) {
  // Split by option markers — handles blank lines between options
  const parts = body.split(/\s*\n\s*([A-D])\s*[.、．)）]\s*/);
  let stem = parts[0].trim().replace(/\n{3,}/g, '\n\n'); // collapse excessive blank lines

  // Clean up HTML code blocks in stem for display
  stem = stem.replace(/<pre><code>([\s\S]*?)<\/code><\/pre>/g, function(m, code) {
    return '<pre><code>' + code.replace(/<[^>]+>/g, '') + '</code></pre>';
  });

  const options = [];

  for (let i = 1; i < parts.length; i += 2) {
    const letter = parts[i];
    const text = (parts[i + 1] || '').trim().replace(/\s+/g, ' ');
    options.push(text);
  }

  return { stem, options, correctIndex: null };
}

function parseCodingQuestion(body) {
  // Extract code blocks
  const codeBlocks = [];
  const codeRegex = /```[\s\S]*?```/g;
  let match;
  while ((match = codeRegex.exec(body)) !== null) {
    const block = match[0].replace(/^```\w*\n?/, '').replace(/\n?```$/, '').trim();
    codeBlocks.push(block);
  }

  // Stem is text before first code block
  const stemMatch = body.split(/```/)[0] || body;
  const stem = stemMatch.replace(/\n/g, ' ').trim();

  // Starter code is typically the first code block (with pass/placeholder)
  let starter = '';
  if (codeBlocks.length > 0 && (codeBlocks[0].includes('pass') || codeBlocks[0].includes('# your code') || codeBlocks[0].includes('# TODO'))) {
    starter = codeBlocks[0];
  }

  return { stem, starter, codeBlocks };
}

function parseAnswers(raw) {
  if (!raw) return {};
  const answers = {};
  const lines = raw.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Table format: | num | **X** | explanation |
    const tableMatch = line.match(/^\|\s*(\d+)\s*\|\s*\*{0,2}([A-D]|[^|]*?)\*{0,2}\s*\|/);
    if (tableMatch) {
      const num = parseInt(tableMatch[1]);
      const answer = tableMatch[2].trim();
      // Get explanation from the same row
      const expMatch = line.match(/\|\s*(?:\*{0,2}[^|]*?\*{0,2}\s*\|)\s*(.+?)\s*\|/);
      const explanation = expMatch ? expMatch[1].trim() : '';

      // Detect if it's a code answer or text answer
      if (answer.includes('输出') || answer.includes('打印')) {
        answers[num] = { text: answer, explanation, htmlAnswer: mdToHtml(explanation) };
      } else if (answer.length <= 2 && /^[A-D]$/.test(answer)) {
        // Choice answer - letter only
        answers[num] = { text: answer, explanation, letter: answer };
      } else {
        answers[num] = { text: answer, explanation, htmlAnswer: mdToHtml(explanation) };
      }
    }

    // Code answer format: after "### 编程题 N"
    const codeHeaderMatch = line.match(/^###\s*编程题\s*(\d+)/);
    if (codeHeaderMatch) {
      const num = parseInt(codeHeaderMatch[1]);
      // Collect code block
      let j = i + 1;
      while (j < lines.length && !lines[j].trim().startsWith('```')) j++;
      if (j < lines.length) {
        j++; // skip opening ```
        let code = '';
        while (j < lines.length && !lines[j].trim().startsWith('```')) {
          code += (code ? '\n' : '') + lines[j];
          j++;
        }
        if (!answers[num]) answers[num] = {};
        answers[num].code = code;

        // Try to extract test cases from comments like # 12
        const testCases = extractTestCases(code);
        if (testCases.length > 0) {
          answers[num].testCases = testCases;
        }
        answers[num].fullAnswer = code;
        i = j;
      }
    }
  }

  return answers;
}

function extractTestCases(code) {
  const testCases = [];
  const lines = code.split('\n');

  for (const line of lines) {
    // Match patterns like: func(args)  # expected
    // or: print(func(args))  # expected
    const printMatch = line.match(/print\s*\(\s*(.+?)\s*\)\s*#?\s*(.*)$/);
    if (printMatch) {
      const call = printMatch[1].trim();
      const expected = printMatch[2].trim();
      if (expected && !expected.includes('expected')) {
        testCases.push({
          c: call,
          e: isNaN(expected) ? expected.replace(/['"]/g, '') : Number(expected)
        });
      }
    }
  }
  return testCases;
}

function extractTitle(raw) {
  const firstLines = raw.split('\n').slice(0, 10);
  for (const line of firstLines) {
    const m = line.match(/^#\s+(.+)/);
    if (m) return m[1].trim();
  }
  return '练习平台';
}

function mdToHtml(md) {
  if (!md) return '';
  return md
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>');
}

// ===== MAIN =====
if (require.main === module) {
  const [,, examPath, answersPath, outputPath] = process.argv;
  if (!examPath) {
    console.error('Usage: node parse-exam.js <exam.md> [answers.md] [output.json]');
    process.exit(1);
  }

  const result = parseExam(examPath, answersPath || '');
  const out = outputPath || examPath.replace(/\.md$/, '-data.json');
  fs.writeFileSync(out, JSON.stringify(result, null, 2), 'utf8');
  console.log(`Parsed: ${result.meta.choiceCount} choice, ${result.meta.shortCount} short, ${result.meta.codeCount} code = ${result.meta.total} total`);
  console.log(`Output: ${out}`);
}

module.exports = { parseExam };
