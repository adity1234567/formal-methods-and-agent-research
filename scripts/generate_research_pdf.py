from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf/research_feedback_and_datasets.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
TMP = ROOT / 'tmp/pdfs'
TMP.mkdir(parents=True, exist_ok=True)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCustom', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=colors.HexColor('#17324d'), spaceAfter=10))
styles.add(ParagraphStyle(name='SectionCustom', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=colors.HexColor('#17324d'), spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name='BodyCustom', fontName='Helvetica', fontSize=10.2, leading=14, spaceAfter=7))
styles.add(ParagraphStyle(name='SmallCustom', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=5))
styles.add(ParagraphStyle(name='CellCustom', fontName='Helvetica', fontSize=9, leading=12))
story=[]
def p(text, style='BodyCustom'):
    return Paragraph(text, styles[style])
def add(text, style='BodyCustom'):
    story.append(p(text, style))
def link(label, url):
    return f'<link href="{url}" color="#176b9c"><u>{label}</u></link>'
def table(rows, widths):
    data=[[p(c, 'CellCustom') for c in row] for row in rows]
    t=Table(data, colWidths=widths, hAlign='LEFT', repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef5')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LINEBELOW',(0,0),(-1,0),0.7,colors.HexColor('#a8bbcd')),
        ('LINEBELOW',(0,1),(-1,-1),0.3,colors.HexColor('#dbe3eb')),
    ]))
    story.append(t)
    story.append(Spacer(1,8))

add('Research feedback', 'TitleCustom')
add('Response 1 | Bangla-English LLM agent reliability', 'SmallCustom')
add('<b>The proposed direction is stronger because either outcome can be informative.</b> A study should test whether reliability changes across languages and instruction conditions, without assuming Bangla must perform worse. Perfect performance supports robustness within the tested conditions; it does not establish reliability for every Bangla task.')
add('A focused research question', 'SectionCustom')
add('<b>Does increasing instruction complexity affect task correctness and unintended state changes differently in Bangla and English?</b>')
add('For the current scope, a precise title would be <b>Instruction Complexity and Unintended State Changes in LLM Agents: A Controlled Bangla-English Study</b>. The broader title, <i>Beyond Translation: Measuring the Robustness of Multilingual LLM Agents Under Linguistic Variation</i>, fits a study with wider language and variation coverage.')
table([
    ['<b>Condition</b>', '<b>What to measure</b>'],
    ['Simple / multiple conditions', 'Whether the agent selects exactly the records satisfying the requested conditions.'],
    ['Negation / exceptions', 'Whether the agent preserves excluded records and interprets the scope of the exception correctly.'],
    ['Code-mixing / paraphrases', 'Whether equivalent meaning produces equivalent behavior across wording and language variants.'],
    ['Ambiguity', 'Whether the agent requests the missing information before making a consequential change.'],
], [150, 353])
add('How to make the experiment convincing', 'SectionCustom')
add('<b>Control the comparison.</b> Use matched Bangla and English tasks with identical starting data, tools, permissions, and expected outcomes. Have bilingual reviewers verify meaning. Vary language, logical form, and constraint count deliberately; code-mixing and ambiguity should not automatically be treated as higher complexity.')
add('<b>Check actual behavior.</b> Compare the final environment against independently defined expected changes. Report task success, unintended changes to unrelated records, and appropriate clarification separately. An agent claiming success is insufficient evidence.')
add('<b>Measure robustness and uncertainty.</b> Include paraphrases and repeated runs. Account for the fact that variants and repeated runs of the same underlying task are related observations. If you want to claim equivalent performance, predefine a practically meaningful equivalence margin; a non-significant difference alone does not establish equivalence.')
add('<b>Interpret results within scope.</b> Report which tested variations affect reliability, or evidence of stable performance when no degradation appears. Existing resources such as '+link('XIFBench','https://github.com/zhenyuli801/XIFBench')+' and '+link('WorldBench','https://github.com/OmniAILab/WorldBench')+' provide relevant foundations; their existence means the contribution needs to be the controlled study design and evidence.')

story.append(PageBreak())
add('Dataset availability', 'TitleCustom')
add('Response 2 | Public resources and remaining gaps', 'SmallCustom')
add('<b>Yes, public datasets cover several of these factors.</b> I have not verified one ready-made dataset combining all of them for Bangla-English tool-using agents. The resources below cover different components and require adaptation for a controlled comparison.')
table([
    ['<b>Factor / resource</b>', '<b>Available coverage and limitation</b>'],
    ['Constraints<br/>'+link('XIFBench','https://github.com/zhenyuli801/XIFBench'), 'Instructions with increasing numbers of constraints across six languages. No Bangla. Evaluates generated responses rather than executed actions.'],
    ['Negation<br/>'+link('LLMBar','https://github.com/princeton-nlp/LLMBar'), 'Includes a Negation case-study subset. Useful for evaluating whether judges recognize correct instruction following; it is not an executable Bangla agent benchmark.'],
    ['Ambiguity<br/>'+link('AgentAbstain data','https://huggingface.co/datasets/antiquality/agentabstain')+' | '+link('code','https://github.com/AntiQuality/agentabstain'), '263 matched act/abstain pairs, with 42 executable sandbox environments. English data covers situations where acting or withholding action is appropriate. Bangla adaptation is needed.'],
    ['Bangla / code-mixing<br/>'+link('JobCCC','https://huggingface.co/datasets/Armans33115/JobCCC-Conversational-Job-Recommendation-Bangladesh'), 'English, Bangla, and author-described code-mixed Romanized Banglish conversations: 988 threads per version, with structured constraints. Job recommendation domain; does not directly evaluate deletion or unintended state changes.'],
    ['Unintended changes<br/>'+link('WorldBench','https://github.com/OmniAILab/WorldBench'), '1,600 agent tasks, including checks that unrelated environment state remains unchanged. No Bangla. Localized tasks are not automatically matched translations for isolating language effects.'],
], [150,353])
add('Qualification about LoWAgent', 'SectionCustom')
add('The '+link('LoWAgent paper','https://arxiv.org/abs/2610.27205')+' includes Bengali web-agent tasks, but I have not verified a public dataset download. Treat it as related work until a usable release is confirmed.')
add('Recommended dataset strategy', 'SectionCustom')
add('Adapt an existing agent environment and create a controlled Bangla-English task set. Each underlying task should have:')
for text in [
    'The same starting records and available tools across language versions.',
    'English, Bangla, and code-mixed instructions reviewed for equivalent meaning.',
    'Explicit labels for constraint complexity, negation, exceptions, and ambiguity.',
    'Exact expected changes, plus records that must remain untouched.',
    'An expected clarification response when information needed to act is missing.',
]:
    add('• '+text, 'SmallCustom')
add('This combination could be your contribution. Combining scores from unrelated datasets would not establish a controlled language comparison. The search finding also does not prove that no comparable dataset exists.', 'BodyCustom')
add('Source names in blue are clickable. Prepared from the two research responses in this conversation.', 'SmallCustom')

def footer(c, doc):
    c.setStrokeColor(colors.HexColor('#dbe3eb'))
    c.line(46,39,A4[0]-46,39)
    c.setFont('Helvetica',8)
    c.setFillColor(colors.HexColor('#607386'))
    c.drawString(46,27,'Bangla-English agent research | Feedback and dataset resources')
    c.drawRightString(A4[0]-46,27,str(doc.page))

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=38,bottomMargin=50,title='Research Feedback and Dataset Availability',author='Research notes')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
pdf=pymupdf.open(OUT)
for i,page in enumerate(pdf):
    page.get_pixmap(matrix=pymupdf.Matrix(1.1,1.1)).save(TMP/f'research_response_page_{i+1}.png')
print(f'Created: {OUT}\nPages: {len(pdf)}\nLinks: {sum(len(page.get_links()) for page in pdf)}')
for i,page in enumerate(pdf):
    print(f'Page {i+1}: {len(page.get_text())} characters')
