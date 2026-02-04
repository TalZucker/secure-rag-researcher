"""
Generate a sample security policy PDF for demonstration purposes.
This creates a realistic enterprise security policy document.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime

def create_sample_security_policy():
    """Generate a sample enterprise security policy PDF."""
    
    filename = "data/sample_security_policy.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='darkblue',
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("TechCorp Industries", title_style))
    story.append(Paragraph("Data Security & Privacy Policy", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Version 2.1 | Effective Date: {datetime.now().strftime('%B %Y')}", styles['Normal']))
    story.append(PageBreak())
    
    # Section 1: Introduction
    story.append(Paragraph("Section 1: Introduction", heading_style))
    story.append(Paragraph("""
    This Data Security and Privacy Policy establishes the framework for protecting sensitive 
    information assets at TechCorp Industries. All employees, contractors, and third-party 
    vendors must comply with these requirements to ensure the confidentiality, integrity, 
    and availability of company and customer data.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("""
    The policy applies to all forms of data, including but not limited to: electronic records, 
    physical documents, verbal communications, and data in transit. Violations of this policy 
    may result in disciplinary action up to and including termination of employment or contract.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Section 2: Scope and Definitions
    story.append(Paragraph("Section 2: Scope and Definitions", heading_style))
    story.append(Paragraph("""
    <b>Personally Identifiable Information (PII):</b> Any data that could potentially identify 
    a specific individual, including names, social security numbers, email addresses, phone 
    numbers, financial account numbers, biometric data, and IP addresses.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>Protected Health Information (PHI):</b> Any health information that can be linked to 
    an individual, as defined under HIPAA regulations.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>Confidential Business Information:</b> Trade secrets, proprietary algorithms, customer 
    lists, financial projections, strategic plans, and any information marked as confidential.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Section 3: Data Classification
    story.append(Paragraph("Section 3: Data Classification", heading_style))
    story.append(Paragraph("""
    All data must be classified into one of four categories:
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>Public:</b> Information approved for public disclosure with no restrictions. 
    No special handling required.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>Internal:</b> Information for internal use only. Should not be shared externally 
    without proper authorization. Examples include internal memos, draft documents, and 
    organizational charts.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>Confidential:</b> Sensitive business information requiring protection from unauthorized 
    access. Must be encrypted when stored or transmitted. Access requires business justification 
    and manager approval.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>Restricted:</b> Highly sensitive data including PII, PHI, payment card data, and 
    authentication credentials. Requires maximum protection measures including encryption, 
    access logging, and annual security training for authorized users.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Section 4: PII Handling Requirements (THE KEY SECTION)
    story.append(Paragraph("Section 4: PII Handling Requirements", heading_style))
    story.append(Paragraph("""
    All Personally Identifiable Information (PII) must be handled according to the following 
    mandatory requirements:
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("""
    <b>4.1 Encryption Standards:</b> All PII must be encrypted using AES-256 encryption when 
    stored (data at rest) and TLS 1.3 or higher when transmitted (data in transit). Legacy 
    encryption methods including DES, 3DES, and MD5 hashing are explicitly prohibited.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>4.2 Access Control:</b> Access to PII requires explicit business justification and 
    manager approval within 24 hours of the access request. All access must be logged and 
    reviewed quarterly by the security team. Access must be revoked immediately upon role 
    change or termination.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>4.3 Data Retention:</b> PII must be retained only as long as necessary for business 
    or legal requirements. Specific retention periods are: security audit logs (90 days), 
    customer transaction records (7 years), employee records (7 years post-termination), 
    and marketing data (2 years or until consent is withdrawn).
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>4.4 Secure Disposal:</b> When PII reaches end of retention period, it must be securely 
    destroyed using approved methods: digital data via cryptographic erasure or DOD 5220.22-M 
    standard wiping, physical media via cross-cut shredding or incineration with certificate 
    of destruction.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>4.5 Third-Party Sharing:</b> PII may only be shared with third parties when: (a) required 
    by law, (b) necessary for service delivery with active customer consent, or (c) with vendors 
    who have signed Data Processing Agreements and passed security assessments. All sharing must 
    be documented in the data inventory system.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Section 5: Security Controls
    story.append(Paragraph("Section 5: Technical Security Controls", heading_style))
    story.append(Paragraph("""
    <b>5.1 Authentication:</b> Multi-factor authentication (MFA) is required for all systems 
    accessing confidential or restricted data. Passwords must be minimum 12 characters with 
    complexity requirements and cannot be reused for 24 iterations.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>5.2 Network Security:</b> All production systems must be protected by next-generation 
    firewalls with intrusion detection/prevention enabled. Network segmentation must isolate 
    environments storing PII or payment data. VPN with certificate-based authentication is 
    required for remote access.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("""
    <b>5.3 Vulnerability Management:</b> Critical vulnerabilities must be patched within 
    7 days of disclosure, high severity within 30 days, and medium severity within 90 days. 
    Quarterly vulnerability scans and annual penetration tests are mandatory for all 
    internet-facing systems.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Section 6: Incident Response
    story.append(Paragraph("Section 6: Security Incident Response", heading_style))
    story.append(Paragraph("""
    Any suspected or confirmed security incident involving PII must be reported to the 
    Security Operations Center (SOC) within 1 hour of discovery. The incident response 
    team will assess the breach severity and determine notification requirements.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("""
    For breaches affecting 500 or more individuals, notification to affected parties must 
    occur within 72 hours and regulatory notification (GDPR, CCPA, etc.) within timeframes 
    specified by applicable law. All incidents must be documented in the incident tracking 
    system with root cause analysis completed within 30 days.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Section 7: Compliance and Training
    story.append(Paragraph("Section 7: Compliance and Training", heading_style))
    story.append(Paragraph("""
    Annual security awareness training is mandatory for all employees and contractors. 
    Personnel with access to PII must complete additional privacy training within 30 days 
    of hire and annually thereafter. Training completion is tracked and non-compliance 
    results in access revocation.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("""
    This policy is reviewed and updated annually or when significant changes occur in the 
    regulatory landscape. The Chief Information Security Officer (CISO) is responsible for 
    policy maintenance and enforcement.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("_" * 80, styles['Normal']))
    story.append(Paragraph("""
    <i>This document is classified as Internal Use. Unauthorized distribution is prohibited.</i>
    """, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Sample security policy created: {filename}")
    print(f"📄 Document contains detailed PII handling requirements for RAG demonstration")

if __name__ == "__main__":
    create_sample_security_policy()
