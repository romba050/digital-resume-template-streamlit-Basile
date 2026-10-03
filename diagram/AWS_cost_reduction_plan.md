# AWS cost reduction plan — basile-rommes.com

Written 2026-08-10, from the July 2026 bill (USD 43.26 pre-tax + 10.81 VAT = 54.07).

## Where the money actually goes

| Line item | USD | What it really is |
|---|---:|---|
| Elastic Load Balancing | 16.57 | ALB: $0.0225/hr x 730h = $16.43 base, plus ~$0.14 of LCU |
| Virtual Private Cloud | 13.75 | Public IPv4 addresses at $3.65/mo each. ~4 of them: **3 belong to the ALB**, 1 to EC2 |
| Elastic Compute Cloud | 11.49 | t3.micro at $0.0108/hr = $7.88, plus ~$3.60 EBS (~40 GB gp3) |
| Route 53 | 1.45 | Hosted zone $0.50 + health check + query volume |
| Data Transfer | 0.00 | Traffic is negligible |
| Tax (Swedish VAT 25%) | 10.81 | |
| **Total** | **54.07** | |

**The ALB and its three IP addresses are $27.52 of the $43.26 pre-tax bill — 64%.**

## What the ALB is actually buying

Nothing that is being used, except one thing:

- **Load balancing:** not in use. There is one EC2 instance. There is nothing to balance across.
- **High availability:** not in use. The ALB is spread over three availability zones, but the
  single instance sits in one. If that AZ fails, the site is down regardless.
- **TLS termination with auto-renewing certificates (via ACM):** this *is* real, and it is the
  only benefit currently being paid for. Cost: $27.52/month. Let's Encrypt + certbot does the
  same job for $0.

## Verdict on the "commercial-scale architecture" goal

The current setup does not demonstrate a commercially scalable design — it demonstrates the
shape of one without the substance. An engineer reading the diagram sees a load balancer with a
single target and reads it as cargo-culting, not architecture.

Two honest ways to keep the CV value without the bill:

1. **Document the scaling path.** A cost-justified single-node deployment plus a written
   explanation of exactly what changes at higher traffic (ASG across AZs, ALB in front,
   sticky sessions or externalised Streamlit state, RDS instead of local files) shows more
   judgment than an over-provisioned setup that cannot be defended.
2. **Commit the HA version as Terraform that is never applied.** `terraform plan` output in the
   repo proves the multi-AZ design can be built, at zero running cost. This is a stronger
   portfolio artifact than the running ALB, because it is reviewable code rather than a console
   screenshot.

## Plan A — remove the ALB, terminate TLS on nginx (do this first)

Captures ~$34/month of the ~$41 available. Everything else is a rounding error by comparison.

Projected bill: `EC2 11.49 + IPv4 3.44 + Route53 0.95 = 15.88 pre-tax` → **$19.85/month with VAT**
(down from $54.07; saving ~$34/month, ~$410/year).

Order matters — this sequence has near-zero downtime and a clean rollback at every step:

1. **Lower the DNS TTL** on the `basile-rommes.com` A record to 60 seconds. Wait for the old TTL
   to expire (up to whatever it is now, often 300s or 3600s) before step 5.
2. **Allocate an Elastic IP** and associate it with the instance. The instance already has an
   auto-assigned public IP that is billed at the same rate, so this adds no cost — it makes the
   address stable across stop/start, which the current one is not.
3. **Open ports 80 and 443** to `0.0.0.0/0` in the instance security group. They are currently
   almost certainly restricted to the ALB's security group.
4. **Add TLS to nginx.** Add a `:443` server block with a certbot-issued certificate, and make
   `:80` redirect to `:443` (the ALB does this redirect today). Use the certbot Docker image with
   the HTTP-01 challenge; port 80 must stay reachable for renewals. The existing WebSocket
   proxy headers in the config already work and need no change — important, since most of the
   apps are Streamlit.
5. **Verify over the Elastic IP directly** (`curl -k https://<EIP>/`) *before* touching DNS.
   Check one Streamlit app and the Flask app, since those exercise WebSockets and long
   inference timeouts respectively.
6. **Repoint the Route 53 A record** from the ALB alias to the Elastic IP. Both paths are live
   at this moment, so there is no outage window.
7. **Watch for 24 hours**, then delete the ALB, its target group, and the Route 53 health check.
   The three IPv4 charges stop when the ALB is deleted.
8. **Restore the TTL** to 300s and update the architecture diagram.

Rollback at any point before step 7: the ALB is still live and the DNS record can be pointed
back at it.

The ACM certificate can be left in place — unused ACM certificates are free.

## Plan B — further trimming (optional, after A is stable)

Projected: **~$12.70/month with VAT.** Diminishing returns, more risk, do only if motivated.

- **1-year EC2 Instance Savings Plan**, no upfront: roughly 30% off the instance. Zero technical
  risk; the only cost is a 12-month commitment. ~$2.40/month saved.
- **t3.micro → t4g.micro** (ARM/Graviton): $0.0086/hr vs $0.0108/hr, ~20% cheaper. Requires
  rebuilding every Docker image for `linux/arm64`. **Check PyTorch and any wheels first** —
  this is where it can bite. Do it on a scratch instance before committing.
- **Shrink the EBS volume** from ~40 GB to ~16 GB: ~$2/month. Fiddly (requires creating a new
  volume and copying), and the least worthwhile item here.

## On the $5/month target

Not reachable on AWS. The floor is set by two unavoidable costs: one public IPv4 address at
$3.65/month, and an always-on instance at $4.40–6.30/month. With VAT that is ~$11–13/month even
after every optimisation above.

Getting to ~$5 means leaving AWS — a Hetzner CX22 is about EUR 3.79/month including IPv4 and
comfortably outperforms a t3.micro. But that trades away the thing the setup exists to
demonstrate. Recommendation: treat ~$13/month as the real target and keep the AWS story.

(A CloudFront-in-front-of-IPv6-only-origin design would dodge the IPv4 charge — CloudFront
gained IPv6 origin support in September 2025 and its 1 TB/month free tier would cover this
traffic. It is not recommended here: it adds a caching layer in front of WebSocket-heavy
Streamlit apps, which is exactly the kind of fiddly failure mode that is not worth $3.65/month.)
