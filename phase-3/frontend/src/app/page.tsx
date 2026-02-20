"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import ThemeToggleButton from "@/components/ui/ThemeToggleButton";

export default function Home() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push("/dashboard");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="landing-page">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="landing-nav">
          <div className="landing-logo">
            <div className="logo-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M9 11l3 3L22 4" />
                <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
              </svg>
            </div>
            <span className="logo-text">TodoPro</span>
          </div>
          <div className="landing-nav-actions">
            <Link href="/login" className="nav-link">
              Sign In
            </Link>
            <Link href="/register" className="btn btn-primary btn-sm">
              Get Started
            </Link>
            <ThemeToggleButton />
          </div>
        </div>
      </header>

      <main className="landing-main">
        {/* Hero Section */}
        <section className="hero-section">
          <div className="hero-container">
            <div className="hero-left">
              <div className="hero-badge">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
                <span>Task Management Made Simple</span>
              </div>
              <h1 className="hero-title">
                Organize Your Work,<br />Achieve Your Goals
              </h1>
              <p className="hero-subtitle">
                A beautiful, intuitive task manager that helps you stay focused and productive without the complexity.
              </p>
              <div className="hero-actions">
                <Link href="/register" className="btn btn-primary">
                  Get Started Free
                </Link>
                <Link href="/login" className="btn btn-secondary">
                  Sign In
                </Link>
              </div>
            </div>
            <div className="hero-right">
              <div className="hero-visual">
                <div className="visual-card visual-card-1">
                  <div className="card-header">
                    <div className="card-status card-status-active"></div>
                    <span className="card-title">Design Review</span>
                  </div>
                  <div className="card-content">
                    <div className="card-line card-line-long"></div>
                    <div className="card-line card-line-medium"></div>
                  </div>
                </div>
                <div className="visual-card visual-card-2">
                  <div className="card-check-wrapper">
                    <div className="card-check">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    </div>
                    <span className="card-check-label">Task Completed</span>
                  </div>
                  <div className="card-content">
                    <div className="card-line card-line-medium"></div>
                    <div className="card-line card-line-short"></div>
                  </div>
                </div>
                <div className="visual-card visual-card-3">
                  <div className="card-icon-wrapper">
                    <div className="card-icon">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="10" />
                        <polyline points="12 6 12 12 16 14" />
                      </svg>
                    </div>
                    <div className="card-line card-line-short"></div>
                  </div>
                </div>
                <div className="visual-floating-element visual-element-1"></div>
                <div className="visual-floating-element visual-element-2"></div>
                <div className="visual-gradient-bg"></div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="features-section">
          <div className="section-header">
            <h2 className="section-title">Simple, Powerful Features</h2>
            <p className="section-description">Everything you need to manage your tasks effectively</p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 11l3 3L22 4" />
                  <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
                </svg>
              </div>
              <h3>Easy Task Management</h3>
              <p>Create, organize, and track your tasks with a clean and intuitive interface.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 6v6l4 2" />
                </svg>
              </div>
              <h3>Stay Organized</h3>
              <p>Keep track of your progress and never miss an important deadline.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
                </svg>
              </div>
              <h3>Secure & Private</h3>
              <p>Your data is protected with enterprise-grade security and encryption.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" />
                </svg>
              </div>
              <h3>Team Collaboration</h3>
              <p>Share tasks and collaborate seamlessly with your team members.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
                  <path d="M13.73 21a2 2 0 01-3.46 0" />
                </svg>
              </div>
              <h3>Smart Reminders</h3>
              <p>Get timely notifications to stay on top of your important tasks.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                  <path d="M8 21h8M12 17v4" />
                </svg>
              </div>
              <h3>Cross-Platform Sync</h3>
              <p>Access your tasks anywhere, anytime across all your devices.</p>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="how-it-works">
          <div className="section-header">
            <h2 className="section-title">How It Works</h2>
            <p className="section-description">Get started in minutes and transform the way you work</p>
          </div>

          <div className="steps-container">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <h3>Create Your Account</h3>
              <p>Sign up in seconds with your email. No credit card required.</p>
            </div>
            <div className="step-arrow">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" />
                </svg>
              </div>
              <h3>Add Your Tasks</h3>
              <p>Create tasks with titles, descriptions, and organize them your way.</p>
            </div>
            <div className="step-arrow">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <div className="step-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
              </div>
              <h3>Get Things Done</h3>
              <p>Track progress, complete tasks, and achieve your goals efficiently.</p>
            </div>
          </div>
        </section>


        {/* CTA Section */}
        <section className="cta-section">
          <div className="cta-content">
            <div className="cta-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z" />
                <path d="M2 17l10 5 10-5" />
                <path d="M2 12l10 5 10-5" />
              </svg>
            </div>
            <h2 className="cta-title">Ready to Transform Your Productivity?</h2>
            <p className="cta-description">Start your journey today.</p>
            <div className="cta-actions">
              <Link href="/register" className="btn btn-primary btn-large">
                Get Started Free
              </Link>
              <Link href="/login" className="btn btn-secondary btn-large">
                Sign In
              </Link>
            </div>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <div className="logo-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M9 11l3 3L22 4" />
                  <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
                </svg>
              </div>
              <span className="logo-text">TodoPro</span>
            </div>
            <p className="footer-tagline">The modern task management solution for productive individuals and teams.</p>
            <div className="footer-social">
              <a href="#" className="social-link" aria-label="Twitter">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" />
                </svg>
              </a>
              <a href="#" className="social-link" aria-label="GitHub">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22" />
                </svg>
              </a>
              <a href="#" className="social-link" aria-label="LinkedIn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z" />
                  <circle cx="4" cy="4" r="2" />
                </svg>
              </a>
            </div>
          </div>
          <div className="footer-links">
            <div className="footer-section">
              <h4>Product</h4>
              <ul>
                <li><Link href="/register">Get Started</Link></li>
                <li><Link href="#features">Features</Link></li>
                <li><Link href="#pricing">Pricing</Link></li>
                <li><Link href="#updates">Updates</Link></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Company</h4>
              <ul>
                <li><Link href="#about">About Us</Link></li>
                <li><Link href="#careers">Careers</Link></li>
                <li><Link href="#contact">Contact</Link></li>
                <li><Link href="#blog">Blog</Link></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Resources</h4>
              <ul>
                <li><Link href="#help">Help Center</Link></li>
                <li><Link href="#docs">Documentation</Link></li>
                <li><Link href="#api">API</Link></li>
                <li><Link href="#community">Community</Link></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Legal</h4>
              <ul>
                <li><Link href="#privacy">Privacy Policy</Link></li>
                <li><Link href="#terms">Terms of Service</Link></li>
                <li><Link href="#security">Security</Link></li>
                <li><Link href="#cookies">Cookie Policy</Link></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2026 TodoPro. All rights reserved.</p>
          <div className="footer-bottom-links">
            <Link href="#privacy">Privacy</Link>
            <Link href="#terms">Terms</Link>
            <Link href="#sitemap">Sitemap</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
