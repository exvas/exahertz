app_name = "exahertz"
app_title = "Exahertz"
app_publisher = "sammish"
app_description = "trading"
app_email = "sammish.thundiyil@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/exahertz/css/exahertz.css"
# app_include_js = "/assets/exahertz/js/exahertz.js"

# include js, css files in header of web template
# web_include_css = "/assets/exahertz/css/exahertz.css"
# web_include_js = "/assets/exahertz/js/exahertz.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "exahertz/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Invoice" : "public/js/sales_invoice.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "exahertz/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "exahertz.utils.jinja_methods",
#	"filters": "exahertz.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "exahertz.install.before_install"
# after_install = "exahertz.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "exahertz.uninstall.before_uninstall"
# after_uninstall = "exahertz.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "exahertz.utils.before_app_install"
# after_app_install = "exahertz.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "exahertz.utils.before_app_uninstall"
# after_app_uninstall = "exahertz.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "exahertz.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"exahertz.tasks.all"
#	],
#	"daily": [
#		"exahertz.tasks.daily"
#	],
#	"hourly": [
#		"exahertz.tasks.hourly"
#	],
#	"weekly": [
#		"exahertz.tasks.weekly"
#	],
#	"monthly": [
#		"exahertz.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "exahertz.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "exahertz.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "exahertz.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["exahertz.utils.before_request"]
# after_request = ["exahertz.utils.after_request"]

# Job Events
# ----------
# before_job = ["exahertz.utils.before_job"]
# after_job = ["exahertz.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"exahertz.auth.validate"
# ]
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Customer-custom_customer_id",
                    "Customer-custom_consumer_id",
                    "Sales Invoice-custom_consumer_id",
                    "Sales Invoice-custom_meter_reading_date",
                    "Sales Invoice-custom_invoice_month_and_year",
                    "Sales Invoice Item-custom_from",
                    "Sales Invoice Item-custom_to_date",
                    "Sales Invoice Item-custom_days",
                    "Sales Invoice Item-custom_watts",
                    "Customer-custom_account_no",
                    "Customer-custom_meter_p69",
                    "Sales Invoice-custom_account_no",
                    "Sales Invoice-custom_meter_p69",
                    "Sales Invoice-custom_print_currency",
                    "Sales Invoice-custom_print_exchange_rate",
                    "Sales Invoice-custom_print_in_words",
                    "Sales Invoice-custom_print_amount_usd"
                ]
            ]
        ]
    }
]