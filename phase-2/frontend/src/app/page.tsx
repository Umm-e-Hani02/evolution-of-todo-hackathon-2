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
          <h1 className="landing-logo">TodoPro</h1>
          <div className="landing-nav-actions">
            <Link href="/login" className="btn btn-secondary">
              Sign In
            </Link>
            <ThemeToggleButton />
          </div>
        </div>
      </header>

      <main className="landing-main">
        {/* Hero Section */}
        <section className="hero-section">
          <div className="hero-content">
            <div className="hero-text">
              <h1 className="hero-title">Streamline Your Tasks, Amplify Your Productivity</h1>
              <p className="hero-subtitle">
                The ultimate task management platform built for teams and individuals who demand security, efficiency, and simplicity.
              </p>
              <div className="hero-actions">
                <Link href="/register" className="btn btn-primary btn-large">
                  Start Free Trial
                </Link>
                <Link href="/login" className="btn btn-secondary btn-large">
                  Sign In
                </Link>
              </div>
              <div className="hero-stats">
                <div className="stat-item">
                  <span className="stat-number">10K+</span>
                  <span className="stat-label">Active Users</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">99.9%</span>
                  <span className="stat-label">Uptime</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">24/7</span>
                  <span className="stat-label">Support</span>
                </div>
              </div>
            </div>
            <div className="hero-visual">
              <div className="dashboard-preview">
                <div className="preview-header">
                  <div className="preview-tabs">
                    <div className="tab active">Dashboard</div>
                    <div className="tab">Tasks</div>
                    <div className="tab">Settings</div>
                  </div>
                  <div className="preview-controls">
                    <div className="control-btn"></div>
                    <div className="control-btn"></div>
                    <div className="control-btn"></div>
                  </div>
                </div>
                <div className="preview-content">
                  <div className="preview-task">
                    <div className="preview-checkbox"></div>
                    <div className="preview-task-info">
                      <h4>Complete project proposal</h4>
                      <p>Finish the quarterly project proposal document</p>
                    </div>
                    <div className="preview-badge">High Priority</div>
                  </div>
                  <div className="preview-task completed">
                    <div className="preview-checkbox checked"></div>
                    <div className="preview-task-info">
                      <h4>Team meeting preparation</h4>
                      <p>Prepare agenda and materials for team sync</p>
                    </div>
                    <div className="preview-badge completed">Done</div>
                  </div>
                  <div className="preview-task">
                    <div className="preview-checkbox"></div>
                    <div className="preview-task-info">
                      <h4>Client presentation</h4>
                      <p>Prepare slides for the important client meeting</p>
                    </div>
                    <div className="preview-badge">Medium</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="features-section">
          <div className="section-header">
            <h2 className="section-title">Powerful Features for Maximum Efficiency</h2>
            <p className="section-description">Everything you need to organize, track, and complete your tasks effectively</p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🔐</div>
              <h3>Bank-Level Security</h3>
              <p>Enterprise-grade encryption and JWT authentication ensure your data stays private and secure.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">👥</div>
              <h3>Multi-User Isolation</h3>
              <p>Each user gets their own private workspace with complete data separation and privacy.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Lightning Fast</h3>
              <p>Optimized for speed and performance with instant task updates and real-time sync.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3>Mobile Ready</h3>
              <p>Seamlessly access your tasks from any device with our responsive design.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Smart Insights</h3>
              <p>Track your productivity with built-in analytics and task completion insights.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔄</div>
              <h3>Real-Time Sync</h3>
              <p>All your tasks update instantly across all devices and platforms.</p>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="how-it-works">
          <div className="section-header">
            <h2 className="section-title">Simple Workflow, Powerful Results</h2>
            <p className="section-description">Get started in seconds and boost your productivity immediately</p>
          </div>

          <div className="steps-container">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Create Account</h3>
              <p>Sign up in less than a minute with your email</p>
            </div>
            <div className="step-divider"></div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>Add Tasks</h3>
              <p>Create and organize your tasks with titles and descriptions</p>
            </div>
            <div className="step-divider"></div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Track Progress</h3>
              <p>Monitor your progress and stay productive every day</p>
            </div>
            <div className="step-divider"></div>
            <div className="step">
              <div className="step-number">4</div>
              <h3>Stay Organized</h3>
              <p>Maintain focus and achieve your goals consistently</p>
            </div>
          </div>
        </section>

        {/* Testimonials */}
        <section className="testimonials-section">
          <div className="section-header">
            <h2 className="section-title">Trusted by Productive Professionals</h2>
            <p className="section-description">Join thousands of users who have transformed their productivity</p>
          </div>

          <div className="testimonials-grid">
            <div className="testimonial-card">
              <div className="testimonial-content">
                <p>"This platform has completely transformed how our team manages projects. The security features give us peace of mind while the intuitive interface keeps everyone productive."</p>
              </div>
              <div className="testimonial-author">
                <div className="author-avatar">JD</div>
                <div className="author-info">
                  <h4>John Doe</h4>
                  <p>Product Manager</p>
                </div>
              </div>
            </div>
            <div className="testimonial-card">
              <div className="testimonial-content">
                <p>"As someone who values privacy, I love the multi-user isolation. I can trust that my personal tasks remain completely separate from others, even on shared systems."</p>
              </div>
              <div className="testimonial-author">
                <div className="author-avatar">JS</div>
                <div className="author-info">
                  <h4>Jane Smith</h4>
                  <p>Software Engineer</p>
                </div>
              </div>
            </div>
            <div className="testimonial-card">
              <div className="testimonial-content">
                <p>"The simplicity combined with powerful features makes this my go-to task manager. It's helped me increase my productivity by 40% in just one month!"</p>
              </div>
              <div className="testimonial-author">
                <div className="author-avatar">MR</div>
                <div className="author-info">
                  <h4>Mike Roberts</h4>
                  <p>Freelancer</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="cta-section">
          <div className="cta-content">
            <h2 className="cta-title">Ready to Transform Your Productivity?</h2>
            <p className="cta-description">Join thousands of professionals who have already revolutionized their task management workflow</p>
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
          <div className="footer-section">
            <h3>TodoPro</h3>
            <p>The ultimate task management solution for productive teams and individuals.</p>
          </div>
          <div className="footer-section">
            <h4>Product</h4>
            <ul>
              <li><Link href="#">Features</Link></li>
              <li><Link href="#">Pricing</Link></li>
              <li><Link href="#">Security</Link></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Company</h4>
            <ul>
              <li><Link href="#">About</Link></li>
              <li><Link href="#">Contact</Link></li>
              <li><Link href="#">Privacy</Link></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Support</h4>
            <ul>
              <li><Link href="#">Help Center</Link></li>
              <li><Link href="#">Documentation</Link></li>
              <li><Link href="#">Community</Link></li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2026 TodoPro. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
