---
title: "Module 4 - Implementation"
layout: default
nav_order: 13
---

# Module 4: Implementation & Fieldwork

<div class="alert alert-info">
<strong>Duration:</strong> 2 weeks | <strong>Effort:</strong> 10-12 hours | <strong>Level:</strong> Applied
</div>

---

## 📋 Overview

With your experimental design complete, it's time to bring your SP survey to life. This module covers the critical transition from design blueprints to live data collection. You'll learn to configure online survey platforms, conduct rigorous pilot testing, navigate ethics approvals, manage field logistics, and implement quality assurance protocols that ensure your data is reliable and actionable.

Implementation is where theory meets practice—and where many surveys succeed or fail. This module provides the practical skills and checklists you need to launch a professional-grade SP study.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

1. **Configure** advanced survey logic in platforms like Qualtrics, SurveyCTO, and LimeSurvey including randomization, piping, quotas, and embedded data
2. **Design and execute** comprehensive pilot testing protocols including cognitive interviews, usability testing, and statistical validation
3. **Navigate** ethics approval processes (IRB/REB) and implement GDPR-compliant data protection measures
4. **Develop** detailed recruitment plans with realistic timelines, budgets, and multi-channel strategies
5. **Implement** automated data quality safeguards including attention checks, timer validation, device fingerprinting, and GPS verification
6. **Create** real-time monitoring dashboards to track completion rates, quota fulfillment, and data quality flags

---

## 🛠️ Survey Platform Configuration

### Platform Selection Criteria

| Platform | Best For | Cost | Learning Curve | Advanced Features |
|----------|----------|------|----------------|-------------------|
| **Qualtrics** | Academic/enterprise, complex logic | $$$$ (institutional) | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ Excellent |
| **SurveyCTO** | Field research, offline capability | $$ | ⭐⭐ Easy | ⭐⭐⭐⭐ Good |
| **LimeSurvey** | Open-source, budget-conscious | Free | ⭐⭐⭐⭐ Steep | ⭐⭐⭐ Fair |
| **Sawtooth** | CBC/conjoint specialists | $$$$ | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ Excellent |
| **Google Forms** | Simple surveys only | Free | ⭐ Very easy | ⭐ Limited |

**Recommendation for SP Research:** Qualtrics (if available) or SurveyCTO for serious studies; LimeSurvey for learning/pilots.

### Qualtrics Configuration Walkthrough

#### Step 1: Import Experimental Design

**Prepare CSV file from Ngene/R:**

```csv
TaskID,BlockID,AltID,Price,Time,Frequency,Comfort
1,1,A,2.5,30,10,1
1,1,B,3.5,25,15,0
2,1,A,4.0,35,8,0
2,1,B,2.5,40,12,1
...
```

**Import to Qualtrics:**
1. Survey Flow → Add Embedded Data
2. Upload design matrix as "Loop & Merge" file
3. Map columns to embedded data fields: `${e://Field/Price_A}`, `${e://Field/Time_A}`, etc.

#### Step 2: Randomization Logic

**Block Randomization:**

```javascript
// Qualtrics JavaScript: Assign random block
Qualtrics.SurveyEngine.addOnload(function() {
    var blockID = Math.floor(Math.random() * 3) + 1; // Blocks 1-3
    Qualtrics.SurveyEngine.setEmbeddedData('AssignedBlock', blockID);
});
```

**Display Logic:**
- Show choice tasks only if `BlockID == AssignedBlock`
- Randomize order of choice tasks within block
- Randomize left/right position of alternatives

#### Step 3: Dynamic Question Text with Piping

**Question Text:**

```
Which option would you choose for your regular commute?

Option A:
- Fare: ${e://Field/Price_A}
- Travel Time: ${e://Field/Time_A} minutes
- Wait Time: ${e://Field/Frequency_A} minutes
- Comfort: ${e://Field/Comfort_A_Text}

Option B:
- Fare: ${e://Field/Price_B}
- Travel Time: ${e://Field/Time_B} minutes
- Wait Time: ${e://Field/Frequency_B} minutes
- Comfort: ${e://Field/Comfort_B_Text}

○ Option A
○ Option B
○ Neither (I would not use transit)
```

**Comfort Text Mapping (using JavaScript):**

```javascript
Qualtrics.SurveyEngine.addOnReady(function() {
    var comfortA = "${e://Field/Comfort_A}";
    var comfortText = (comfortA == "1") ? "Seats available" : "Standing room";
    Qualtrics.SurveyEngine.setEmbeddedData('Comfort_A_Text', comfortText);
});
```

#### Step 4: Quota Management

**Setting Quotas:**

1. Tools → Quotas → New Quota
2. Define: "Urban Commuters" = 400 completes
3. Logic: `Location == 1 AND Status == "Complete"`
4. Action when met: "Display quota full message" or "Skip to end"

**Cross-Quotas:**

```
Quota Matrix:
              Income <50k  |  Income 50-100k  |  Income >100k
Urban           120              180                100
Suburban        100              150                 90
Rural            60               70                 30
```

**Implementation:**
- Create 9 separate quotas
- Use branching logic to assign quota category early in survey
- Display real-time quota status (optional)

#### Step 5: Data Validation

**Custom Validation Rules:**

**Travel Time Reasonableness:**
```javascript
// Ensure reported travel time is realistic
var time = parseInt("${q://QID2/ChoiceTextEntryValue}");
if (time < 1 || time > 300) {
    return "Please enter a travel time between 1 and 300 minutes.";
}
```

**Income Consistency:**
```javascript
// Check household income vs. vehicle ownership
var income = parseInt("${q://QID5/SelectedChoicesRecode}");
var vehicles = parseInt("${q://QID6/ChoiceTextEntryValue}");
if (income < 30000 && vehicles > 3) {
    // Flag for review, don't block
    Qualtrics.SurveyEngine.setEmbeddedData('IncomeVehicleFlag', 1);
}
```

### SurveyCTO Configuration

**Advantages for SP Research:**
- Works offline (mobile data collection)
- GPS coordinate capture
- Device ID tracking
- Encrypted data storage
- Excellent for in-person intercepts

**Basic Choice Task in SurveyCTO Syntax:**

```
begin group: choice_task_1
    note: You are choosing between two bus routes.

    begin group: option_a
        note: **Option A**
        note: Fare: ${fare_a}
        note: Time: ${time_a} minutes
        note: Frequency: Every ${freq_a} minutes
    end group

    begin group: option_b
        note: **Option B**
        note: Fare: ${fare_b}
        note: Time: ${time_b} minutes
        note: Frequency: Every ${freq_b} minutes
    end group

    select_one choice: Which would you choose?
        1 Option A
        2 Option B
        3 Neither
end group
```

**GPS Capture:**
```
type: geopoint
name: interview_location
label: Capture location (automatic)
required: yes
```

### Common Platform Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Slow loading with large designs** | Pre-load design matrix, use session storage |
| **Mobile responsiveness issues** | Test on 3+ devices, use CSS media queries |
| **Quota overfill** | Set "soft close" at 95%, hard close at 100% |
| **Respondent sees same task twice** | Implement task ID tracking, skip if already shown |
| **Piping errors with special characters** | Sanitize all piped text, escape HTML entities |
| **Data export format inconsistencies** | Define export schema before launch, test with pilot data |

---

## 🧪 Pilot Testing Protocols

### The Three-Stage Pilot Approach

#### Stage 1: Internal Testing (n = 5-10)

**Who:** Research team members, colleagues

**Objectives:**
- Identify technical bugs (broken links, logic errors)
- Test survey flow and branching
- Verify data export format
- Check mobile compatibility

**Duration:** 1-2 days

**Checklist:**
- [ ] Survey loads on desktop (Chrome, Firefox, Safari, Edge)
- [ ] Survey loads on mobile (iOS, Android)
- [ ] All questions display correctly
- [ ] Randomization works as intended
- [ ] Piping shows correct values
- [ ] Skip logic functions properly
- [ ] Data exports to usable format (CSV/Excel)
- [ ] Quota tracking works
- [ ] Consent and incentive delivery works

**Bug Log Template:**

| Bug ID | Severity | Description | Steps to Reproduce | Status |
|--------|----------|-------------|-------------------|--------|
| 001 | High | Q5 not displaying on iPhone | Open survey on iOS Safari, go to Q5 | Fixed |
| 002 | Medium | Piped text shows ${error} | Select Option A in Task 3 | In progress |

#### Stage 2: Cognitive Interviews (n = 8-12)

**Who:** Representative sample from target population

**Objectives:**
- Assess comprehension of instructions
- Identify confusing wording
- Evaluate cognitive burden
- Gauge realistic completion time
- Gather qualitative feedback on attribute relevance

**Method: Think-Aloud Protocol**

**Script:**
```
"I'm going to ask you to complete this survey while thinking out loud.
Please say whatever comes to mind as you read each question and make
your choices. There are no wrong answers—I want to understand how
you're interpreting everything.

I'll occasionally ask:
  • What are you thinking right now?
  • Can you explain why you chose that?
  • Was anything unclear or confusing?

Let's begin..."
```

**Observation Checklist:**

- [ ] Did respondent understand choice task instructions on first reading?
- [ ] Did they notice the practice task feedback?
- [ ] Did they comment on realism of scenarios?
- [ ] Did they exhibit decision fatigue (complaints, random clicking)?
- [ ] Did they understand attribute definitions?
- [ ] Did they ask clarifying questions?
- [ ] Did they struggle with any specific question types?

**Probing Questions:**

1. "On a scale of 1-10, how realistic did those scenarios feel?"
2. "Which attributes mattered most to you? Why?"
3. "Were there any attributes you wished you could see but weren't included?"
4. "Did you feel rushed or bored at any point?"
5. "Is there anything you'd change about the survey?"

**Debrief Form:**

```
Cognitive Interview Debrief (Respondent #____)

1. Completion Time: _____ minutes

2. Comprehension Issues (list question IDs):
   _________________________________________________

3. Suggestions for Improvement:
   _________________________________________________

4. Realism Rating (1-10): _____

5. Overall Comments:
   _________________________________________________

6. Would participate in real survey: Yes / No / Maybe
```

**Analysis:**
- Identify questions where >25% of participants struggled
- Note common misconceptions or interpretation errors
- Flag attributes that were ignored or caused confusion
- Assess whether completion time matches expectations

#### Stage 3: Soft Launch (n = 50-100)

**Who:** Real respondents from recruitment channels

**Objectives:**
- Test full survey flow at scale
- Validate data quality checks
- Assess completion/dropout rates
- Identify edge cases in real data
- Calibrate incentives and messaging

**Duration:** 3-5 days

**Monitoring Metrics:**

| Metric | Target | Pilot Result | Action if Below Target |
|--------|--------|--------------|------------------------|
| **Completion Rate** | >75% | 68% | Reduce length or improve incentive |
| **Median Time** | 15-20 min | 22 min | Cut non-essential questions |
| **Quota Balance** | ±10% of target | Urban: 120%, Rural: 40% | Adjust recruitment ads |
| **Attention Check Pass** | >90% | 85% | Review check difficulty |
| **Data Quality Flags** | <5% | 8% | Tighten validation rules |

**Data Quality Checks to Run:**

1. **Straight-lining:** >80% of Likert responses are same value
2. **Speeding:** Completion time < 50% of median
3. **Response Consistency:** Contradictory answers (e.g., "Never use transit" but reports 5 trips/week)
4. **Impossible Values:** Negative income, 500-minute commute
5. **Open-Text Gibberish:** Random characters in open-ends

**Soft Launch Debrief:**

- Review top 5 most common data quality flags
- Examine dropout patterns (which question loses most respondents?)
- Assess whether attribute levels are generating variation in choices
- Check for dominant alternatives (>80% choose same option every time)
- Validate that quotas are filling at expected rates

**Go/No-Go Decision Criteria:**

✅ **Proceed to Full Launch if:**
- Completion rate ≥ 70%
- Median time within ±20% of target
- Data quality flags < 10%
- No critical technical bugs
- Quota recruitment is feasible

⛔ **Pause and Revise if:**
- Completion rate < 60%
- >15% of data flagged for quality issues
- Recruitment cost per complete >50% over budget
- Choice data shows no variation (everyone picking same alternative)

---

## 📋 Ethics & Compliance

### IRB/REB Approval Process

**Timeline:** Allow 4-8 weeks for review

**Required Documents:**

1. **Protocol Summary**
   - Research objectives
   - Sample description
   - Recruitment methods
   - Data collection procedures
   - Data security measures
   - Risk assessment

2. **Informed Consent Form**
   - Study purpose and sponsor
   - What participants will do
   - Time required
   - Compensation details
   - Risks and benefits
   - Privacy protections
   - Voluntary participation statement
   - Contact information
   - Consent mechanism (checkbox, signature)

3. **Survey Instrument**
   - Full questionnaire
   - All branching logic documented
   - Screenshots of key screens

4. **Recruitment Materials**
   - Email templates
   - Social media ads
   - Flyers/posters
   - Screening scripts

5. **Data Management Plan**
   - Storage location and encryption
   - Access controls
   - Retention period
   - De-identification procedures
   - Disposal methods

**Example Informed Consent Text:**

```
INFORMED CONSENT FOR RESEARCH

Study Title: Metropolitan Transit Preference Study
Principal Investigator: Dr. Jane Smith, Department of Civil Engineering
Sponsor: City Transportation Department

PURPOSE:
You are invited to participate in a research study about public
transit preferences. This study will help the city design better
transit services. Approximately 1,000 people will participate.

PROCEDURES:
If you agree to participate, you will:
  • Answer questions about your current travel (5 minutes)
  • Compare hypothetical transit options (10 minutes)
  • Provide demographic information (3 minutes)
  • Total time: approximately 15-20 minutes

COMPENSATION:
You will receive a $10 Amazon gift card upon completion.

RISKS:
There are no anticipated risks beyond those in everyday life.

BENEFITS:
You may not directly benefit, but your input will help improve
local transit services. You will gain insight into how transport
planning decisions are made.

CONFIDENTIALITY:
Your responses will be kept confidential. Data will be stored on
encrypted servers accessible only to the research team. Results
will be reported in aggregate only—no individual responses will
be identifiable. Data will be retained for 5 years, then securely
deleted.

VOLUNTARY PARTICIPATION:
Your participation is completely voluntary. You may skip questions
or withdraw at any time without penalty. Your decision will not
affect your relationship with the university or transit agency.

QUESTIONS:
For questions about the study, contact Dr. Jane Smith at
jsmith@university.edu or 555-0123.

For questions about your rights as a research participant, contact
the Institutional Review Board at irb@university.edu or 555-0199.

CONSENT:
☐ I have read the above information
☐ I am 18 years or older
☐ I agree to participate in this study

[Proceed to Survey] [Decline]
```

### GDPR Compliance (for EU respondents)

**Key Requirements:**

1. **Lawful Basis:** Consent must be freely given, specific, informed, unambiguous
2. **Right to Access:** Respondents can request their data
3. **Right to Erasure:** "Right to be forgotten"
4. **Data Minimization:** Collect only necessary data
5. **Purpose Limitation:** Use data only for stated purposes
6. **Storage Limitation:** Delete when no longer needed

**GDPR-Compliant Consent:**

```
DATA PROTECTION NOTICE

We collect the following personal data:
  • Responses to survey questions
  • Approximate location (city/region)
  • Device type and IP address (for fraud prevention)

Legal basis: Your consent

We will use this data to:
  • Conduct transportation research
  • Improve public transit services
  • Publish aggregate statistical findings

Your data will be stored securely for 5 years, then deleted.

You have the right to:
  ✓ Access your data
  ✓ Correct errors
  ✓ Request deletion
  ✓ Withdraw consent
  ✓ Lodge a complaint with supervisory authority

To exercise these rights, contact: dpo@university.edu

☐ I consent to the collection and use of my data as described

[Continue] [Decline]
```

### Vulnerable Populations

**Additional Protections Needed for:**

- **Children (<18):** Parental consent required
- **Elderly:** Large font, simplified language, phone support
- **Non-Native Speakers:** Translated materials, language assistance
- **Low-Income:** Ensure compensation is fair but not coercive
- **Cognitively Impaired:** Simplified consent, guardian involvement

---

## 🎯 Recruitment & Fieldwork Logistics

### Multi-Channel Recruitment Strategy

#### Channel 1: Online Panels (e.g., Lucid, Dynata, Prolific)

**Pros:**
- Fast (can reach target n in days)
- Built-in quota management
- Quality screening tools
- Payment/incentive handling automated

**Cons:**
- Expensive ($5-$15 per complete)
- "Professional respondents" may rush
- Sample may not match general population
- Limited demographic reach (skews younger, urban)

**Setup Process:**
1. Create project brief with quotas
2. Set quality thresholds (completion rate, attention checks)
3. Launch soft launch (n=50)
4. Review quality metrics
5. Full launch

**Cost Estimate:**
- Base price: $8/complete
- Length penalty: +$2 for 15+ minute surveys
- Incidence rate: +$3 if <50% qualify
- Total: ~$10-13/complete
- For n=1,000: $10,000-$13,000

#### Channel 2: Social Media Advertising

**Platforms:** Facebook/Instagram, Reddit, LinkedIn

**Pros:**
- Lower cost ($2-$5/complete)
- Precise demographic targeting
- Can reach niche populations
- Builds brand awareness

**Cons:**
- Slower ramp-up
- Requires ad management skills
- Variable quality
- Platform fees + incentives

**Facebook Ad Targeting Example:**

```
Campaign: Transit Survey - Urban Commuters

Targeting:
  • Location: Within 20 miles of Downtown Metro Area
  • Age: 25-54
  • Interests: Public Transportation, Commuting, Urban Living
  • Behaviors: Commuters, Daily Public Transit Users

Ad Creative:
  Headline: "Help Improve Our Transit System – Get $10"
  Text: "Take a 15-minute survey about your commute. Your input
         will shape future bus and rail improvements."
  Image: Modern bus/train with diverse riders
  Call to Action: "Take Survey"

Budget: $500
Expected Reach: 5,000-8,000
Expected Clicks: 250-400 (5% CTR)
Expected Completes: 125-200 (50% conversion)
Cost per Complete: $2.50-$4.00
```

**Quality Control for Social Media Recruits:**
- Add device fingerprinting (prevent duplicates)
- Require email verification
- Use ZIP code validation
- Slower payout (3-5 days after validation)

#### Channel 3: In-Person Intercepts

**Best for:**
- Transit riders (intercept at stations)
- Specific geographic areas
- Hard-to-reach populations
- Mixed-mode (combine with online follow-up)

**Logistics:**

**Staffing:**
- 2-3 interviewers per location
- Shifts: 4 hours (morning/evening peak)
- Training: 2-hour session on approach, screening, device setup

**Equipment:**
- Tablets (10+) with survey pre-loaded
- Mobile hotspot (backup internet)
- Printed consent forms
- Incentive gift cards
- Clipboards with screener
- Team t-shirts/badges

**Sample Screener Script:**

```
"Hi, I'm [NAME] from [UNIVERSITY]. We're conducting a quick survey
about transit services and offering a $10 gift card for 15 minutes
of your time. Would you be interested?"

[If YES:]
"Great! First, a few quick questions to see if you qualify:

1. Are you 18 or older? (must be YES)
2. Do you use public transit at least once per week? (must be YES)
3. Have you taken this survey before? (must be NO)

[If qualifies:]
"Perfect! Here's a tablet—the survey takes about 15 minutes.
I'll be nearby if you have any questions."

[Upon completion:]
"Thank you! Here's your $10 Amazon gift card. If you'd like to
share feedback, my email is on this card."
```

**Intercept Budget (n=300):**
- Interviewer wages: 6 people × 20 hours × $25/hr = $3,000
- Incentives: 300 × $10 = $3,000
- Equipment rental: 10 tablets × 2 weeks × $15/day = $420
- Permits (station access): $200
- Training & supervision: $500
- **Total: ~$7,120 ($23.73/complete)**

#### Channel 4: Partner Organizations

**Examples:**
- Employer partnerships (survey employees)
- Community groups (email listservs)
- Transit rider councils
- Neighborhood associations

**Pros:**
- Trusted messenger effect (higher response)
- Can reach specific populations
- Often free or low-cost
- Authentic engagement

**Cons:**
- Slower negotiations
- May require IRB amendments
- Limited control over timing
- Potential for bias (self-selected activists)

**Partnership Request Template:**

```
Subject: Research Partnership Opportunity – Transit Survey

Dear [ORGANIZATION CONTACT],

I am conducting research on public transit preferences for the
[CITY] Transportation Department. We are seeking input from
residents to help design better services.

Partnership Opportunity:
  • Share survey link with your [members/employees/subscribers]
  • Survey takes 15 minutes
  • $10 incentive for participants
  • Results shared with your organization
  • No cost to you

What We Need:
  • Email blast to your list (we'll draft text)
  • OR: Social media post (template provided)
  • OR: Link on your website

Timeline: Survey live [DATES]

Benefits to Your Community:
  • Direct input on transit improvements
  • Summary report with findings
  • Recognition in final publication

Would you be interested in discussing this? I'm happy to meet
at your convenience.

Best regards,
[NAME]
[TITLE]
[CONTACT INFO]
```

### Field Timeline & Gantt Chart

**Typical 8-Week Field Period:**

```
Week 1: Soft Launch
  ├─ Day 1-2: Internal testing
  ├─ Day 3-4: Cognitive interviews
  └─ Day 5-7: Soft launch (n=50), monitor hourly

Week 2: Analysis & Adjustments
  ├─ Review pilot data
  ├─ Make survey edits
  ├─ Finalize recruitment channels
  └─ Prepare full launch

Week 3-6: Full Field
  ├─ Daily monitoring (completion, quotas, quality)
  ├─ Adjust recruitment spend based on fill rates
  ├─ Send reminder emails (if panel/email lists)
  └─ Weekly progress reports to stakeholders

Week 7: Final Push
  ├─ Boost ads for hard-to-fill quotas
  ├─ Send final reminder emails
  └─ Close survey when n reached

Week 8: Data Cleaning
  ├─ Export raw data
  ├─ Apply quality filters
  ├─ Check for duplicates
  └─ Prepare dataset for analysis
```

---

## 🔍 Data Quality Assurance

### Automated Quality Checks

#### Check 1: Attention/Trap Questions

**Example:**

```
To ensure data quality, please select "Strongly Agree" for this question.

Strongly Disagree [1] [2] [3] [4] [5] Strongly Agree

[If respondent selects anything other than 5, flag for review]
```

**Placement:** Embed 1-2 in middle of survey (not at beginning)

**Action if Failed:**
- Soft approach: Warning message, allow to continue
- Hard approach: Terminate survey, no incentive

**Debate:** Some researchers argue trap questions are punitive and may cause attrition. Alternative: Use behavioral flags (speeding, straightlining) instead.

#### Check 2: Speeding Detection

**Method:**

```javascript
// Qualtrics: Calculate survey time
var surveyTime = ${e://Field/Q_TotalDuration}; // in seconds
var medianTime = 900; // 15 minutes

if (surveyTime < (medianTime * 0.5)) {
    Qualtrics.SurveyEngine.setEmbeddedData('SpeedFlag', 1);
}
```

**Thresholds:**
- Extreme speeders: <40% of median time → Auto-flag, no payment
- Moderate speeders: 40-60% of median → Flag for manual review
- Acceptable: >60% of median

**Per-Question Timing:**

```javascript
// Flag if spent <2 seconds on choice task
Qualtrics.SurveyEngine.addOnPageSubmit(function() {
    var pageTime = this.getPageTime();
    if (pageTime < 2) {
        Qualtrics.SurveyEngine.setEmbeddedData('Task3_FastClick', 1);
    }
});
```

#### Check 3: Straight-Lining

**Definition:** Selecting same response for all items in a matrix

**Example:**

```
Rate your agreement with the following statements (1=Strongly Disagree, 5=Strongly Agree):

1. I enjoy using public transit       [1] [2] [3] [4] [5]
2. Transit is reliable in my city     [1] [2] [3] [4] [5]
3. I would use transit more often     [1] [2] [3] [4] [5]
4. Transit is affordable              [1] [2] [3] [4] [5]
5. I feel safe on public transit      [1] [2] [3] [4] [5]

[If all responses are "3" or all are "5", flag]
```

**Detection:**

```r
# R code to detect straight-lining
detect_straightline <- function(responses) {
    # responses is a vector of answers
    if (length(unique(responses)) == 1) {
        return(TRUE)  # All same
    } else if (sd(responses) == 0) {
        return(TRUE)  # No variation
    } else {
        return(FALSE)
    }
}
```

**Action:** Flag if >70% of grid questions are straight-lined

#### Check 4: Open-End Gibberish

**Examples of Low-Quality Open-Ends:**
- "asdfasdf"
- "N/A"
- "."
- "hhhhh"
- "none"

**Validation Rules:**

```javascript
// Check minimum word count
var response = "${q://QID10/ChoiceTextEntryValue}";
var wordCount = response.split(/\s+/).length;

if (wordCount < 3) {
    return "Please provide at least a few words.";
}

// Check for repeated characters
if (/(.)\1{4,}/.test(response)) {
    return "Please provide a thoughtful response.";
}
```

**Manual Review:** Sample 10% of open-ends for quality assessment

#### Check 5: Geolocation Verification

**Purpose:** Ensure respondents are in target area (if geographic quotas)

**SurveyCTO GPS Capture:**

```
type: geopoint
name: location
required: yes

[Then check in data:]
lat/long falls within target region boundary
```

**Qualtrics IP-Based Location:**

```javascript
// Use embedded data from Qualtrics
var city = "${loc://City}";
var region = "${loc://RegionName}";

if (city != "TargetCity" && region != "TargetRegion") {
    Qualtrics.SurveyEngine.setEmbeddedData('LocationMismatch', 1);
}
```

**Privacy Note:** Disclose location tracking in consent form

#### Check 6: Duplicate Prevention

**Methods:**

1. **Email Address:** Require unique email
2. **Device Fingerprint:** Browser + OS + Screen Resolution hash
3. **IP Address:** Flag if same IP completes multiple times (allow 2-3 for households)

**Qualtrics Prevent Ballot Box Stuffing:**

Settings → Survey Options → "Prevent Ballot Box Stuffing"
- Cookies
- IP address
- Both (recommended)

**Manual Deduplication:**

```r
# R: Remove duplicates based on multiple criteria
library(dplyr)

survey_data <- survey_data %>%
    group_by(email, ip_address) %>%
    filter(row_number() == 1) %>%  # Keep first occurrence
    ungroup()
```

### Real-Time Monitoring Dashboard

**Tools:** Power BI, Tableau, Google Data Studio, R Shiny

**Key Metrics to Display:**

1. **Completion Funnel**
   ```
   Started: 1,250
   ├─ Consented: 1,180 (94%)
   ├─ Qualified: 950 (76%)
   ├─ Reached Choice Tasks: 890 (71%)
   └─ Completed: 780 (62%)

   Current completion rate: 62%
   ```

2. **Quota Status**
   ```
   Overall: 780 / 1,000 (78%)

   By Segment:
   ┌─────────────┬────────┬────────┬──────────┐
   │ Segment     │ Target │ Actual │ % Filled │
   ├─────────────┼────────┼────────┼──────────┤
   │ Urban       │   400  │   360  │   90%    │
   │ Suburban    │   450  │   310  │   69%  ⚠ │
   │ Rural       │   150  │    110 │   73%    │
   └─────────────┴────────┴────────┴──────────┘
   ```

3. **Data Quality Flags**
   ```
   Total Responses: 780

   Flagged for:
   ├─ Speeding: 45 (5.8%)
   ├─ Straight-lining: 23 (2.9%)
   ├─ Failed attention check: 18 (2.3%)
   ├─ Location mismatch: 12 (1.5%)
   └─ Duplicate IP: 8 (1.0%)

   Clean responses: 674 (86.4%)
   ```

4. **Daily Progress**
   ```
   [Line chart showing completions per day]

   Day 1: 45
   Day 2: 78
   Day 3: 92
   Day 4: 105
   Day 5: 88
   ...

   Projected completion date: May 15 (on track)
   ```

5. **Device Breakdown**
   ```
   Desktop: 62%
   Mobile: 35%
   Tablet: 3%

   [Mobile completion rate: 58% vs. Desktop: 68%]
   ⚠ Consider mobile UX improvements
   ```

**Dashboard Update Frequency:** Every 4-6 hours during active field period

**Alert Triggers:**
- Completion rate drops below 60%
- Any quota >15% behind target
- Quality flags exceed 10%
- Daily completions drop >30% from previous day

---

## 🌍 Real-World Case Studies

### Case Study 1: Chicago Transit Authority Customer Satisfaction SP Study

**Challenge:** Launch large-scale SP survey (n=5,000) across diverse population

**Implementation Approach:**

**Platform:** Qualtrics with custom JavaScript

**Recruitment:**
- 60% online panel (Dynata)
- 25% in-person intercepts at 12 rail stations
- 15% email invitation to CTA rider database

**Pilot Testing:**
- Stage 1: Internal (n=8), found 6 logic errors
- Stage 2: Cognitive interviews (n=10), revised 4 questions
- Stage 3: Soft launch (n=100), adjusted quota targets

**Quality Assurance:**
- 3 attention checks
- GPS verification for in-person interviews
- Manual review of flagged responses (n=230, rejected 120)

**Field Timeline:**
- Week 1-2: Pilot
- Week 3-8: Main field
- Week 9: Data cleaning

**Challenges Encountered:**

1. **Low completion rate in panel (58%)**
   - Solution: Increased incentive from $10 to $15, rate jumped to 72%

2. **Rural quota underfilling**
   - Solution: Targeted Facebook ads in collar counties, achieved target

3. **Mobile abandonment at choice tasks**
   - Solution: Simplified choice card layout for small screens

**Results:**
- Final n = 5,120 (2% over target)
- 87% clean data rate
- Average completion time: 18 minutes
- Total cost: $78,500 ($15.32/complete)

**Lessons Learned:**
- Always pilot on mobile devices
- Build in 20% buffer for quality exclusions
- Monitor quotas daily—late adjustments are expensive

### Case Study 2: European EV Adoption Multi-Country Study

**Challenge:** Coordinate SP survey across 6 countries with varying regulations

**Implementation Complexity:**

**Platforms:**
- Primary: LimeSurvey (open-source, GDPR-compliant)
- Backup: Local vendors in each country

**Ethics/Compliance:**
- 6 separate IRB approvals (3-7 weeks each)
- GDPR compliance required:
  - Data stored on EU servers only
  - Explicit consent for each data use
  - Right to erasure mechanism
  - Data protection officer appointed

**Translation:**
- Survey translated to 6 languages
- Back-translation validation
- Cultural adaptation (e.g., km vs. miles, € vs. £ vs. SEK)

**Recruitment:**
- Each country used local panel provider
- Screened for car ownership + purchase intent

**Pilot Testing:**
- Centralized cognitive interviews (English, n=8)
- Local pilots in each country (n=20 each)
- Found translation issues in German and Swedish versions

**Quality Control:**
- Centralized monitoring dashboard
- Country-specific QA leads
- Weekly coordination calls

**Challenges:**

1. **GDPR Right to Erasure Request**
   - 3 respondents requested data deletion mid-study
   - Solution: Documented process, deleted within 48 hours

2. **VPN Detection**
   - Panel respondents using VPNs failed location checks
   - Solution: Added manual verification step, accepted if IP country matched reported country

3. **Quota Misalignment**
   - Spain oversampled urban residents (85% vs. target 65%)
   - Solution: Applied post-stratification weights

**Results:**
- Final n = 3,600 (600 per country)
- 91% clean data rate
- Avg completion: 22 minutes
- Total cost: €112,000 (€31/complete)

**Key Takeaway:** International studies require 2-3x the coordination time; build in extra buffer.

### Case Study 3: Rural Dial-a-Ride Pilot with Elderly Population

**Challenge:** Survey elderly residents (65+) with limited tech literacy

**Implementation Adaptations:**

**Platform:** Mixed-mode
- Online: SurveyCTO (large fonts, simple interface)
- Phone: CATI (Computer-Assisted Telephone Interview)
- Paper: Mailed surveys with postage-paid return

**Recruitment:**
- Senior centers (flyers, in-person presentations)
- Local newspaper ads
- Word of mouth

**Accessibility Features:**
- Font size: 16pt minimum
- High contrast (black text on white)
- No complex branching
- Phone support hotline (9am-5pm)
- Option to complete over multiple sessions

**Pilot Testing:**
- Tested with senior focus group (n=12)
- Revised language (removed jargon like "modal shift")
- Added definitions for "on-demand," "app-based booking"

**In-Person Assistance:**
- Stationed volunteers at senior centers
- Helped with technical issues, but didn't influence responses

**Quality Assurance:**
- Relaxed speeding thresholds (elderly read more slowly)
- No attention checks (caused confusion in pilot)
- Manual verification of paper surveys

**Results:**
- Final n = 240
- Mode breakdown: 45% paper, 35% phone, 20% online
- Completion rate: 82% (higher than expected)
- Avg time: 28 minutes
- Cost: $38/complete (labor-intensive)

**Lessons:**
- Mixed-mode is essential for elderly populations
- Personal touch increases trust and participation
- Extra time yields higher quality data

---

## ⚙️ Session Breakdown

### Session 1: Platform Configuration & Pilot Design (4 hours)

**Part 1: Qualtrics Live Demo (90 min)**

**Activity:**
1. Instructor imports sample design matrix
2. Builds 3 choice tasks with piping and randomization
3. Sets up quota logic
4. Adds data validation
5. Tests on mobile device
6. Students follow along in their own accounts

**Part 2: Pilot Protocol Workshop (90 min)**

**Task:** Design complete pilot testing plan for assigned scenario

**Deliverables:**
- Internal testing checklist (20 items minimum)
- Cognitive interview script (5 probing questions)
- Soft launch monitoring plan (5 key metrics)

**Part 3: Ethics Discussion (60 min)**

**Case Study Analysis:**
Present 3 scenarios with ethical issues:

1. **Scenario A:** Researcher wants to track GPS without disclosure
   - Discussion: Is this ever acceptable? What disclosure is needed?

2. **Scenario B:** Incentive is $50 for low-income population
   - Discussion: Is this coercive? What's appropriate compensation?

3. **Scenario C:** Survey collects race/ethnicity but doesn't explain why
   - Discussion: What justification is needed? How to build trust?

**Outcome:** Draft consent form for student's own project

### Session 2: Quality Assurance & Field Management (4 hours)

**Part 1: Data Quality Deep Dive (60 min)**

**Exercise:** Analyze pilot dataset (provided) with quality issues

**Dataset includes:**
- n=100 simulated responses
- 15 flagged for speeding
- 8 straight-lined grid questions
- 5 failed attention checks
- 3 duplicate IPs

**Task:**
1. Apply decision rules (keep/reject)
2. Calculate clean data rate
3. Project impact on full study (if 10% rejection, need to recruit 1,100 for n=1,000)
4. Recommend adjustments to survey/recruitment

**Part 2: Dashboard Building Lab (90 min)**

**Tools:** Excel, Google Sheets, or Tableau (depending on student access)

**Activity:**
Create monitoring dashboard with:
- Completion funnel
- Quota status table
- Quality flag summary
- Daily progress chart

**Data provided:** Simulated field data (7 days, 350 completes)

**Challenge:** Identify the problem day and diagnose root cause

**Part 3: Recruitment Plan Simulation (60 min)**

**Scenario:** You have $15,000 budget, 8 weeks, need n=1,000

**Channels available:**
- Online panel: $12/complete, fast
- Social media ads: $4/complete, slower
- In-person intercepts: $25/complete, high quality

**Constraints:**
- At least 30% must be from low-income households (harder to recruit)
- Geographic quotas: Urban 50%, Suburban 35%, Rural 15%

**Task:**
1. Build recruitment mix
2. Create week-by-week timeline
3. Calculate total cost
4. Identify risk mitigation strategies

**Presentation:** Teams present their plans, class votes on most feasible

**Part 4: Troubleshooting Clinic (30 min)**

**Common Issues & Solutions:**

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| "Completion rate tanked on Day 3" | Check for technical issue, media coverage | Review server logs, pause if needed |
| "Urban quota at 120%, rural at 40%" | Recruitment channels skewed | Reallocate ad spend, boost rural targeting |
| "Median time jumped from 15 to 35 min" | New respondents reading more carefully, or survey got longer | Check if questions were added, validate |
| "Quality flags spiked to 25%" | Panel provider sent low-quality sample | Contact provider, request replacement |

---

## 🔬 Lab Activities

### Activity 1: Pilot Debrief Fishbowl (90 minutes)

**Objective:** Experience survey from respondent perspective and identify issues

**Setup:**
- 5 students volunteer as "respondents"
- Rest of class observes (can't speak)
- Instructor moderates

**Process:**

1. **Respondents complete survey** while thinking aloud (20 min)
   - Observers take notes on friction points

2. **Debrief interview** (30 min)
   - Moderator asks each respondent:
     - What was confusing?
     - What felt unrealistic?
     - Would you recommend changes?

3. **Observer report-out** (20 min)
   - Each observer shares top 2-3 issues noticed
   - Class clusters issues into themes

4. **Revision planning** (20 min)
   - Class votes on top 5 issues to fix
   - Brainstorm solutions for each
   - Assign priority (must-fix vs. nice-to-have)

**Deliverable:** Revised survey outline with changes highlighted

### Activity 2: Quality Assurance Audit (60 minutes)

**Objective:** Apply QA criteria to real pilot data

**Provided Materials:**
- Pilot dataset (n=150)
- Data dictionary
- Quality flag definitions

**Tasks:**

**Task 1: Flag Identification (20 min)**

Calculate rates of:
- Speeders (<50% median time)
- Straight-liners (80%+ same response in grids)
- Attention check failures
- Duplicates (same email or IP)

**Task 2: Decision Matrix (20 min)**

For each flagged respondent, decide:
- Auto-reject (clear violation)
- Manual review needed
- Accept with caveat
- Accept clean

**Task 3: Impact Analysis (20 min)**

- Calculate rejection rate
- Assess impact on quotas (which segments most affected?)
- Project additional recruitment needed
- Recommend survey adjustments to reduce future flags

**Deliverable:** QA report (2 pages) with recommendations

---

## 📝 Assignment

### [Module 4 Pilot & Implementation Plan](../assignments/04_pilot_plan.md)

**Objective:** Produce a field-ready implementation package

**Components:**

**1. Survey Screenshots (5-8 pages)**
- Consent screen
- Screening questions
- Instructions for choice tasks
- Example choice task (fully programmed)
- Debriefing section
- Thank you / incentive delivery

**Annotations:** Highlight randomization, piping, validation rules

**2. Pilot Testing Protocol (3 pages)**

Include:
- **Internal testing checklist** (15+ items)
- **Cognitive interview script** (introduction, think-aloud prompts, 5 debrief questions)
- **Soft launch plan** (sample size, duration, monitoring metrics, go/no-go criteria)

**3. Ethics Documentation (4 pages)**

- **Informed consent form** (full text)
- **Data security plan** (storage, access, retention, disposal)
- **IRB submission checklist** (what documents needed)

**4. Recruitment Plan (3 pages)**

- **Target sample and quotas** (table format)
- **Channel strategy** (% allocation across 2-3 channels)
- **Timeline** (Gantt chart or week-by-week plan)
- **Budget** (cost per complete by channel, total)

**5. Quality Assurance Plan (2 pages)**

- **Automated checks** (speeding, attention, validation rules)
- **Monitoring dashboard** (wireframe or screenshot)
- **Decision rules** (when to flag, when to reject)
- **Contingency actions** (what if completion rate drops, quotas don't fill, etc.)

**Submission Requirements:**
- Combined PDF, 20-25 pages
- Include any survey platform code/syntax in appendix
- Filename: `M4_implementation_plan_<lastname>.pdf`
- **Due:** End of Week 7

**Evaluation Rubric (100 points):**

| Component | Points | Criteria |
|-----------|--------|----------|
| Survey implementation | 25 | Screenshots show working logic, professional design, accessible |
| Pilot protocol | 20 | Comprehensive testing plan, realistic timeline, clear go/no-go criteria |
| Ethics compliance | 20 | Complete consent, addresses risks, GDPR-aware (if applicable) |
| Recruitment strategy | 20 | Feasible plan, reasonable budget, multi-channel approach |
| Quality assurance | 15 | Automated checks specified, monitoring plan detailed, decision rules clear |

---

## 💬 Discussion Prompts

**Post your responses on the course forum (200-250 words each; respond to 2 peers):**

### Prompt 1: Incentive Ethics

**Question:**
"How should incentive strategies adapt for hard-to-reach populations (e.g., ride-hail drivers, freight operators, executives)? When does compensation become coercive vs. appropriate?"

**Consider:**
- Time value varies across populations
- Power dynamics (employer-sponsored surveys)
- Cultural norms around payment
- Budget constraints vs. fairness

**Example:** "A $10 incentive may be coercive for someone earning minimum wage but insufficient for a busy executive..."

### Prompt 2: Quality vs. Quantity Trade-off

**Question:**
"What data quality indicators will trigger a pause or redesign in your fieldwork? How do you balance strict quality standards with budget/timeline pressures?"

**Scenarios:**
- Completion rate is 55% (target was 75%)
- 18% of responses are flagged for quality issues
- Quotas are filling unevenly—urban at 95%, rural at 30%

**Discuss:** At what threshold do you stop and fix vs. push through?

### Prompt 3: Mixed-Mode Dilemma

**Question:**
"You're surveying a diverse population: some are tech-savvy, others prefer paper or phone. How do you design a survey that works across modes without compromising data comparability?"

**Challenges:**
- Visual choice cards don't translate to phone interviews
- Paper surveys can't randomize
- Mode effects (people answer differently by mode)
- Cost differences (phone is 5x more expensive)

**Propose:** A mixed-mode strategy with quality controls

---

## 📖 Recommended Resources

### Core Textbooks & Guides

1. **AAPOR (2016).** *Standard Definitions: Final Dispositions of Case Codes and Outcome Rates for Surveys* (9th ed.)
   - Industry standard for calculating response rates
   - [Free download](https://www.aapor.org/Standards-Ethics/Standard-Definitions.aspx)

2. **Dillman, D. A., Smyth, J. D., & Christian, L. M. (2014).** *Internet, Phone, Mail, and Mixed-Mode Surveys: The Tailored Design Method*
   - Chapters 8-10: Implementation and field management
   - Best practices for maximizing response rates

3. **Groves, R. M., et al. (2009).** *Survey Methodology* (2nd ed.)
   - Chapter 7: Data collection methods
   - Chapter 9: Nonresponse in surveys

### Platform Documentation

- **Qualtrics Support: Advanced Survey Logic**
  [https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/)
  - Randomization, embedded data, quotas

- **SurveyCTO Documentation**
  [https://docs.surveycto.com/](https://docs.surveycto.com/)
  - Form design, data quality, offline collection

- **LimeSurvey Manual**
  [https://manual.limesurvey.org/](https://manual.limesurvey.org/)
  - Open-source survey platform guide

### Ethics & Compliance

- **Belmont Report** (1979) - Foundational ethics principles
  [https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/)

- **GDPR Official Text**
  [https://gdpr-info.eu/](https://gdpr-info.eu/)
  - European data protection regulation

- **ESOMAR Guidelines on Online Research**
  [https://www.esomar.org/](https://www.esomar.org/)
  - Professional standards for market research

### Data Quality

- **Meade, A. W., & Craig, S. B. (2012).** "Identifying careless responses in survey data." *Psychological Methods*, 17(3), 437-455.
  - Statistical methods for detecting low-quality responses

- **Curran, P. G. (2016).** "Methods for the detection of carelessly invalid responses in survey data." *Journal of Experimental Social Psychology*, 66, 4-19.

---

## ✅ Module Completion Checklist

Before moving to Module 5, ensure you have:

- [ ] Attended or watched both sessions (8 hours total)
- [ ] Completed Qualtrics configuration walkthrough or equivalent
- [ ] Participated in pilot debrief fishbowl activity
- [ ] Conducted QA audit on sample dataset
- [ ] Posted to all 3 discussion prompts with peer responses
- [ ] Submitted Module 4 Implementation Plan
- [ ] Reviewed IRB submission requirements for your institution
- [ ] Drafted informed consent form for your project
- [ ] Created monitoring dashboard template

**Self-Assessment Questions:**

1. **Can you configure** basic survey logic (randomization, piping, quotas) in at least one platform?
2. **Can you design** a three-stage pilot testing protocol with clear go/no-go criteria?
3. **Can you identify** common data quality issues and apply decision rules?
4. **Can you develop** a multi-channel recruitment plan with realistic budget?
5. **Can you draft** an IRB-compliant informed consent form?

If you answered "yes" to all five—you're ready for Module 5: Discrete Choice Modeling!

---

## 🔗 Navigation

- **Previous:** [Module 3 - Experimental Design & Efficient Choice Tasks](03-experimental-design.md)
- **Next:** [Module 5 - Discrete Choice Modeling & Estimation](05-modeling.md)
- **Related:** [Assignment 4](../assignments/04_pilot_plan.md) | [Syllabus](../syllabus.md) | [Course Home](../index.md)

---

<div class="alert alert-success">
<strong>💡 Pro Tip:</strong> Create a "Field Operations Checklist" with every task from survey launch to data delivery. Include contact info for your survey platform support, panel provider, IT helpdesk, and IRB office. When issues arise mid-field (and they will!), you'll thank yourself for having everything in one place.
</div>

---

**Questions or feedback?** Contact the instructor or post in the course discussion forum.
