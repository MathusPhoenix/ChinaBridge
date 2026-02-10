# ChinaBridge Academy - Translations Guide

## How to Edit Thai Translations

1. Open the file: `translations.js`
2. Find the `th:` section (around line 20)
3. Edit the Thai text in the quotes. For example:

```javascript
th: {
    nav_courses: 'หลักสูตร',     // <-- Edit this Thai text
    nav_tutors: 'ครูสอน',        // <-- Edit this Thai text
    // ... and so on
}
```

## All Translation Keys

### Navigation & Buttons
- `nav_courses` - "Courses" button
- `nav_tutors` - "Tutors" button
- `nav_pricing` - "Pricing" button
- `nav_login` - "Login" button
- `nav_dashboard` - "My Dashboard" button
- `nav_admin` - "Admin" button
- `nav_logout` - "Logout" button
- `nav_start_learning` - "Start learning" button

### Hero Section (Homepage Top)
- `hero_eyebrow` - Tagline (gray text at top)
- `hero_title` - Main heading
- `hero_subtitle` - Description under main heading
- `hero_explore` - "Explore courses" button
- `hero_become_tutor` - "Become a tutor" button
- `hero_experts` - "expert peer tutors" (stats)
- `hero_satisfaction` - "student satisfaction" (stats)
- `hero_hours` - "hours tutoring" (stats)

### Course Names & Descriptions
- `courses_title` - "Our Courses" heading
- `courses_subtitle` - Subtitle for courses section
- `csca_name` - "CSCA Prep" course name
- `csca_desc` - CSCA course description
- `sat_name` - "SAT Tutoring" course name
- `sat_desc` - SAT course description
- `hsk_name` - "HSK/HSKK & University Prep" course name
- `hsk_desc` - HSK course description

### Features
- `features_tutoring` - "1:1 tutoring sessions"
- `features_custom` - "Customized study plans"
- `features_experts` - "Subject experts available"
- `features_practice` - "Practice test review"
- `features_skill` - "Targeted skill building"
- `features_strategy` - "Strategy sessions"
- `features_hsk` - "HSK levels 1-6 support"
- `features_speaking` - "Speaking & conversation practice"
- `features_interview` - "Interview coaching"

### Tutors Section
- `tutors_title` - "Our Tutors" heading
- `tutors_subtitle` - Tutors section subtitle
- `tutor_phoenix` - Phoenix's name
- `tutor_phoenix_desc` - Phoenix's description
- `tutor_serum` - Serum's name
- `tutor_serum_desc` - Serum's description

### Pricing Section
- `pricing_title` - "Pricing Plans" heading
- `pricing_subtitle` - Pricing section subtitle
- `price_starter` - "Starter" plan name
- `price_bundle` - "Bundle" plan name
- `price_monthly` - "Monthly" plan name
- `price_sessions` - "sessions"
- `price_per_month` - "/month"
- `price_savings` - "savings"
- `price_priority` - "Priority scheduling"
- `price_dedicated` - "Dedicated tutor"
- `price_within` - "Use within"
- `price_3_months` - "3 months"
- `price_buy` - "Buy bundle" button
- `price_start` - "Start today" button

### Login & Registration
- `login_title` - Main login section heading
- `login_subtitle` - Login section description
- `auth_login_tab` - "Login" tab
- `auth_signup_tab` - "Sign Up" tab
- `form_email` - "Email address" label
- `form_password` - "Password" label
- `form_first_name` - "First Name" label
- `form_last_name` - "Last Name" label
- `form_confirm_password` - "Confirm Password" label
- `form_password_hint` - "Create a password (min 6 characters)"
- `btn_login` - "Login" button
- `btn_signup` - "Sign Up" button
- `btn_create_account` - "Create your account" heading
- `link_forgot_password` - "Forgot password?" link
- `link_reset_here` - "Reset it here" link
- `link_sign_up` - "No account? Sign up" link
- `link_sign_in` - "Already have an account? Sign in" link
- `msg_login_success` - Login success message
- `msg_register_success` - Registration success message

### Student Dashboard
- `dashboard_title` - "Student Dashboard" heading
- `dashboard_welcome` - "Welcome back" greeting
- `dashboard_manage` - Dashboard description
- `dashboard_my_courses` - "My Courses" section heading
- `dashboard_my_sessions` - "My Tutoring Sessions" section heading
- `dashboard_available` - "Available Courses" section heading
- `dashboard_no_courses` - "You haven't enrolled in any courses yet" message
- `dashboard_no_sessions` - "No tutoring sessions scheduled" message
- `btn_enroll` - "Enroll" button
- `session_with` - "with" (in session text)
- `session_hours` - "hour(s)" (in session text)

### Admin Dashboard
- `admin_title` - "Admin Dashboard" heading
- `admin_subtitle` - Admin dashboard description
- `admin_total_students` - "Total Students" card
- `admin_total_sessions` - "Total Sessions" card
- `admin_student_list` - "Student List" heading
- `admin_loading` - "Loading students..." message
- `admin_email` - "Email" column header
- `admin_joined` - "Joined" column header

### Footer
- `footer_copyright` - Copyright text
- `footer_quick_links` - "Quick Links" heading
- `footer_contact` - "Contact Us" heading

## Example: Editing a Thai Translation

**Before:**
```javascript
nav_courses: 'หลักสูตร',
```

**After (Custom Thai Translation):**
```javascript
nav_courses: 'คลาส',  // Changed from หลักสูตร to คลาส
```

Save the file, and the changes will appear on your website after you refresh the page.

## Testing Your Changes

1. Edit `translations.js`
2. Push to GitHub: `git push origin main`
3. Wait for Render to redeploy (2-5 minutes)
4. Refresh your website to see the changes
5. Click the language switcher (top right) to toggle Thai/English

---

**Note:** Only edit the Thai text inside the quotes in the `th: { ... }` section. Don't edit the keys (the part before the colon) or the English translations will break.
