# Multi-Agent Orchestration: The Orchestrator Agent

## Introduction

In the generative AI age, **the rate at which you can create and command your agents becomes the constraint of your engineering output.** When your agents are slow, you're slow. When your agents have a problem, you have a problem. If you're using agents at scale, you know exactly what I mean.

Right now, every engineer sits at one of these levels:

- Base agents
- Better agents
- More agents
- Custom agents

The theme here is simple. **At each step, you scale your compute to scale your impact.** It's not about what you can do anymore. It's about what you can teach your agents to do for you.

There's one more level, one giant leap forward I'm going to share with you in this lesson. Engineers like you and I using agents every single day. We're all thinking about the same thing. And the votes for Agentic Horizon show it. **In order to scale your agents, you need to manage your fleets of agents.** Multi-agent orchestration is the next step in our journey as agentic engineers.

So, let me introduce you to one powerful multi-agent orchestration solution. **The one agent to rule them all, the orchestrator agent.**

---

## The Three Pillars of Multi-Agent Orchestration

This is the single interface pattern applied to your fleet of agents. It's an existing engineering paradigm that great engineers have used for decades. We're applying the single interface pattern to agents.

But it's not just the orchestrator agent that matters. We're combining three pillars:

1. **The orchestrator agent** - your unified interface to your agents
2. **CRUD for agents** - your orchestrator agent unlocks CRUD for your agents. This gives you agents at scale
3. **Observability** - for real-time monitoring of your agents performance, costs, and as you'll see, results

When you combine these three, you get a powerful solution to multi-agent orchestration.

---

## Getting Started: The Interface

Where is our input field? This is not a normal application for normal users. This is for you and I, the agentic engineer. We're maximizing information density without losing UX quality.

If we hit `Command+K` here, we'll see our prompt input interface. It has useful metadata about the capabilities of this codebase we'll cover in a moment. We'll just start with a simple ping prompt. Our orchestrator agent is going to, of course, give us a quick response.

---

## Demonstration: Creating and Orchestrating Multiple Agents

### Creating Three Agents

Now, let's spin up some agents here. We're going to create three individual agents. We're going to have them summarize the codebase, build an application structure summary inside of a markdown file with mermaid tables. We're going to fire this off and truly show off the potential and the capability of an orchestrator agent.

Now, our orchestrator agent is going to craft three new agents and then prompt them. So, we're going to have a total of six unique tool calls built around managing and orchestrating agents. As you can see here:

- Here's our first agent
- Here's our second agent
- And our orchestrator agent is going to spin up our third agent

Right now, our QA agent that's going to do both the front end and the backend summarization work. There's our QA agent. And you can see right away, **this is a differentiated agentic coding experience.**

### Observability: Seeing Everything

With multi-agent observability, you can see everything. **Observability is a key component of a successful multi-agent system.** Why is that? It's because:

- If you can't measure it, you can't improve it
- And if you can't measure it, you can't scale it

Okay? If you have 10 agents doing the wrong thing, does it matter that you have 10? Of course not. This is why observability is key. And it's also why the orchestrator is an advanced agent coding concept. It comes last after custom agents.

You can see here we have an interface that is communicating the work of every one of our agents. So we have:

- Responses
- Tools
- Thinking

We can of course filter on any one of these. We can filter on responses, individual tool calls, we can filter on our individual agents. So here's just our QA agent. **The observability here is essential for scaling impact.**

### Scaling Compute

With a single prompt, I've deployed three times the compute an engineer working in the terminal has. Okay. And this is just the beginning. We have two fast agents. We've divided this work into front end, backend, and then we have a primary kind of powerful agent that's going to do the key work of summarizing both the front end and backend.

And our orchestrator took care of actually commanding and creating our agents. If we scroll back up, you can see all six of those tool calls:

- Create agent
- Create agent
- Create agent
- And then three command calls

Already we have this very interesting pattern of our orchestrator agent taking our high-level prompt and then writing out in much more detail the actual concrete work that we want done to our agents. **Already this is a differentiated experience.**

### Orchestrator vs. Sub-Agents

I know right away some engineers are going to think, aren't these just sub agents? Why aren't you just using sub agents? **Having a primary agent here connected to your orchestrator agent is differentiated.** You're going to see this over and over and over. We can do a lot more when we control our agentic units with our orchestrator agent.

And you'll notice throughout all of this, our orchestrator agent has stopped doing work, right? Its orchestration tasks for the meantime is completed. It has created and commanded our agents. Now, our agents are doing the work.

---

## Individual Agent Interface: Managing the Core Four

And if we dial into the individual agent user interface here, you can see a couple of key things:

- We have the name
- We have the status
- We have, of course, the context windows

**We're managing the core four of every single agent we spin up.** If you do not adopt your agents perspective, if you do not know what they can do, you do not know what you can do.

We have:

- Our response messages
- Tool calls
- Hooks
- And of course, we have reasoning

You can see here, none of our agents here are thinking. They're not reasoning at all. That's okay. For these tasks, we of course have our models and of our costs.

---

## Results: Consumed and Produced Assets

Now something incredible just happened. As you can see here, our primary QA agent has finished its work. We have its consumed assets and it's produced assets. **Engineering is all about communicating work. So your multi-agent system should reflect that. It should showcase that.**

And so right here in a single response message, you can see the actual read files and the produced files from our QA agent at a glance. We can do something really powerful. We can of course just see the diff right here in line, but more importantly, **we can one-click into our editor.** So now we're operating inside the loop. We're looking at this file. We're actually reviewing and understanding what's been done in markdown mode.

Here we can see exactly what our agent has broken down for us. And this is a great opportunity to actually talk about the codebase architecture. **You should be compounding your engineering with each leverage point of agent coding that you add to your codebase.** And then you build a system where you find one that lets you solve problems as you continue to move from in-loop to outloop.

**There are so many problems that you do not need to be sitting in the terminal prompting back and forth to solve.**

### Specialized Tools vs. Out-of-the-Box Solutions

All right, keep in mind **a specialized tool like this is going to be more powerful than some out-of-the-box cloud-based tool.** Why is that? It's because these tools are designed for everyone's codebase, not yours. When you build something like this, you get specialization all the way down.

It's super important to note I have this deployed for several code bases. I can access anywhere, anytime through multiple devices, and it's all because it's designed as an outloop system.

You can see our front end and backend agents have also completed their work. We can see all the files they've consumed. We can see the actual concrete produced results. Okay, **you're not getting this with out-of-the-box agent coding tools. You're not getting this with any cloud tool, right?** This is a specialized solution for managing agents at scale. This is multi-agent orchestration.

So, we can dive into any one of these results. You can see here our backend QA agent went pretty hard here on the backend docs. Uh this is all fantastic. We can of course dive into any of this if we want to with a single click and we'll be taken right into the piece of documentation that we can then tweak, delete, modify.

---

## Managing Agents at Scale

Another massive advantage of our orchestration system is this. **It's designed to help us manage our agents at scale.** List agents and then check the status of our agents. Okay. And so this is going to kick off our orchestrator agent once again and have it actually understand the work that was done.

### Protecting Context Windows

Now, this is super important. **Our orchestrator agent is not always looking at the results, right?** I mean, look at what just happened there between all these agents. It's incredibly overwhelming. There's too much information. Okay?

And so what we've done here with our orchestrator agent is that we've designed it to be... this is super important. We're going to touch on this in a moment. We've designed it to be... **it is not always observing the logs. It cannot be. We have to protect its context window.**

This is true for your orchestrator agent. This is true for your primary agents. **You always need to be monitoring and understanding the core four of every agent you boot up.** Remember, you know, on top of every feature, any lab builds, any UI that you see, any experience, it's all just the core four. Don't let anyone confuse you, okay?

**Context, model, prompt, tools.** Do you know what these four leverage points are at every critical moment? All right, this is key.

As you can see here, through our interface, we have a really great idea of the state of the core 4 for all of our agents. Okay. And so you can see here the orchestrator agent, you know, ran some specialized tools to actually check the status of every agent and then it's communicating to us.

All right. So this single interface pattern is very important here for orchestrating agents at scale:

- We're protecting context windows
- We have specialized dedicated focused agents, right? Focused on one specific task. This is important. We're going to touch on that in a moment
- And then our orchestrator agent is communicating to us

Okay, we can continue our work. This is the powerful part of having a system like this. Okay, we can build anything we need to to get the job done.

---

## Enabling Thinking Mode

So, you can see here we have a bunch of metadata. We'll cover that in just a moment. Let's just run this. I'll say "command all agents create one section, a single sentence of each key node in the system. Quick, concise, enable thinking."

All right, so let's get thinking mode turned on here and we'll go ahead and fire that off. So, once again here, the pattern is the same. Prompt one, prompt two, prompt three. We have the brain icon here. And now they're starting to actually think through what's going on here.

This should be just a quick summary. They're going to make a quick change to the top of their file. **These aren't just one-off sub-agents where the context is blown away or we have to kind of manage what or where the sub agent was. These are primary agents that we can tap into over and over until that specific job is done.** Okay.

Something that's going to happen here that's going to be really important. You know, here are results. Once again, we can just dial into these. We can see all the consumed files versus produced files.

**It's important that our orchestrator agent can tap into each agent when it needs to command them, read from them. But again, we don't want our orchestrator agent getting involved in the actual work. It is just here to orchestrate.**

### Reviewing Results

Let's look at our front end summary. So, if we just click into this, uh, we should see a front-end key nodes. So, check this out. We have:

- Our key components
- Our composables
- Our services
- And we have our core files

So this is great, right? We got a key summary here. You can see all the key technologies we used. **We are constantly moving from in-loop to outloop.** And the multi-agent orchestration with the orchestrator agent helps us:

- Reduce our presence
- Understand what our agents are doing
- Scale our agents

---

## Agent Lifecycle: Delete When Done

Now that the job is done, whatever work you needed your agent to complete, it's finished. Okay? There's a journey that every engineer goes through:

1. First, you learn how to read code
2. Then you create code
3. Then you update code
4. And then in the end, you learn that the best code is no code at all. You learn to delete

`Command+K`, delete all agents. **Agentic engineering is no different. You must treat your agents as deletable temporary resources that serve a single purpose.**

You can see three tool calls came in there. Our orchestrator agent has blown away our agents. The work is done. The job is done. **Let the agents go home.**

In tactical agent coding lesson six, we dial into this concept with one key tactic. **This is something that 80% plus of all engineers are rediscovering over and over every time they explode their context window.** Okay, multi-agent orchestration with our orchestrator agent lets us do just that.

### The R&D Framework

What are we doing here? We're tapping into the R&D framework. We discussed this inside of the elite context engineering agent horizon lesson. Okay, by the way, if you haven't completed tactical agent coding and the previous Agent Horizon lessons, stop this video, go watch those. All of this will make a lot more sense.

**We are compounding our engineering with tactics of agentic coding and powerful patterns over and over and over.** Okay? Every single lesson matters. Every single lesson was designed to have a critical idea, a critical tactic to push what you can do further.

You know, let me be clear. **I'm super excited for larger effective context windows, but 200k context window is plenty. You're just stuffing a single agent with too much work, just like your boss did to you at your last job.** Okay? Don't force your agent to context switch. You know what that feels like. **Force it to focus and then let it go home back to the data center. Delete it.** Okay.

---

## How It Works: High-Level Overview

So, how does this work? Let's just take a step back and talk high level. How does this actually work? Um, let me be super clear about something. **The orchestrator agent is... even in single agents a lot of engineers are barely using their agents potential.**

---

## Advanced Example: Scout and Builder Pattern

Okay, I'm going to use our orchestrator scout and build create simple flat colorless gray pills for the app header information tense keyword there. This is a location in the codebase active running logs. This is up here, right? So the running cost displays. So, we're just going to create some simple UI pills. This is a simple one-off task. I just want to showcase this prompt to you.

**We're spinning up a small team of agents to accomplish a task. Each context window. Each task of our agent is going to be focused.** And you can see here this prompt has triggered orchestrator thinking. Okay, our orchestrator is now thinking and now it's running a workflow.

So, there we go. We have our scout header and we're going to have our... you can see we're going to create two agents here. Scout and our builder. So there's our builder, there's our scout, and our scout is going to get to work here after our orchestrator kicks it off.

There we go. **We can spin them up and spin them down with a single prompt.** Okay, this is another powerful example of multi-agent orchestration. We have agents doing work, creating useful information sets, and they're going to pass that off to the next agent.

Okay, so we're talking:

- Plans
- Logs
- Results
- Documentation

And then our orchestrator chains it all together.

### Orchestrator Monitoring Pattern

Look at what our orchestrator is doing here. It is actually involved in this process. Okay, so our orchestrator is in a loop sleeping. You've probably seen this pattern. **Your primary agent will sleep, fire off some other agents to do some work, and then it'll check in on that.** Right? So this is a common agent coding pattern you can use, right?

We're scaling up the compute to monitor this multi-agent workflow. And so every 15 seconds it's going to run check agent status on the scout to see how the scout is doing. And so you can see there scout has just finished this work.

We're now going to get our produced assets, right? **Every agent must produce a concrete result. Otherwise, what's the point?** We can of course dial in. We can see the summary there. And it knows exactly where to put these exact files.

Keep in mind how much work this orchestrator has conducted up to this point. Okay. and his context still floating along because we are indeed all of the context. Now our orchestrator has handed the work off to our builder agent. Okay, very powerful stuff there.

There's another command agent tool and you can see, check out this write up. Check out this detailed write up our orchestrator gave to our builder. **Okay, it is doing some serious prompt engineering.** You can see the work coming in there.

Keep in mind these agents are operating on this project. They're operating on themselves. Builder being very precise because we had a scout look for the changes to make. Obviously, relatively simple UI change, but we're putting a team of agents to make sure the job gets done.

**If you can deploy a little bit more compute to have more confidence and more trust in your agents, why wouldn't you, right?** Compute can solve so many of your engineering problems if you put the compute to work.

Okay, so here we are builder here doing some thinking, right? We can just dial in on all the thinking of our agent here if we want to. And of course, we can just specialize on just our builder agent logs here. If you just want to see the individual tools, we can see that as well. But what we really care about most of all is the results.

Our orchestrator thinking one more time, still executing, doing verification work. Looks great. Changes are in place. It's going to check the syntax for us. All this is happening for us with our multi-agent orchestration system. All driven by our orchestration agent.

---

## The Three Critical Pieces

We have put together three critical pieces to unlock the next scale of agentic engineering:

1. **We have an orchestrator**
2. **We have CRUD for agents** so we can unlock agents at scale
3. **And we have observability**

These three design elements unlock something special here.

---

## Complex Example: UI Changes

We're going to do something a little more complex, some more UI changes. We want our agent list to collapse. And we want to update our orchestrator chat to go into small mode when browser width is less than 650. We'll just be super clear here and say less than. Okay, we're going to kick this off and this is of course going to fire off in an agentic prompt designed for our orchestrator.

### The Investment Trade-Off

This is something that a lot of engineers don't realize. Once you build a custom agent, the real trade-off here, the real balance is that this takes time to build, right? Very obviously multi-agent orchestration and the orchestrator agent cost upfront investment and you have to manage your orchestration agent. You have to manage:

- The plumbing
- The database
- Websocket connections

And it can be a lot to coordinate. Is this worth investing into? Uh I think the answer is a very clear yes.

**You want to have even if you don't use this, the key here is that you want to have some type of outloop agentic coding system, right?** You want to have multiple modes of engineering. If you need to step down into the loop, which I had to do when building this out, I've had to do it multiple times. You can, right? Hop in the loop, hop in the terminal, increase your presence, right? Write those back and forth prompts. That's fine. I fully recognize that is a valid mode of engineering.

**But more and more there is work you should not be doing. You're wasting your time. The right way to think about engineering now is the agentic way. You want to be thinking about scaling your agentics.**

### Human-in-the-Loop Decision Points

Remember tactic eight. **Human in the loop decision points are going to be very critical.** You can see a simple interface on top of this where your agent wants to ask you a question. Your agent wants to prompt you. **This is a key point in agentic engineering where your agents start asking you questions versus the other way around.** Okay.

Something else that's missing. If we want to fork an agent's context window and basically duplicate an agent from a specific point, this is one tool away and thanks to the Cloud Agent SDK, it's a few modules away from being built out.

Uh looks like our builder has finished its work. This is fantastic. You can see again all the work done. One click away, right? **Result-oriented engineering in a single interface, right?** Our outloop system is very very powerful here.

**A lot of systems rely on pull requests. That's great, but it misses a lot of the story. It misses a lot of the journey, right?** We get all of it here with our observability interface.

So our agent's finished. Um let's see how it's done here. So this feature shipped. We're now having our reviewer agent confirm that the work was done. **Big labs are going to be doing something like this, right?** You already see it with cloud coding tools. These are coming. All right?

And there's going to be many varieties of this, right? There's going to be:

- Your vibe coding one-shot prompt tools
- And then there's going to be your legitimate engineering tools

Obviously, we're going to lean super hard on the legitimate software engineering out-of-the-loop agentic coding tools like this system, but these are coming up. **We want to have a spectrum of tools we can use.**

More specifically, **we want to have a dedicated solution for solving our domain specific problems with our specialized agents.** Okay, this is the agentic engineering advantage. **You can build agents that know your problem better than anyone.** Okay, better than any cloud tool, better than any team. This is the advantage. Okay.

**And you can scale it hard now with the multi-agent orchestration and the orchestration agent.**

---

## Conclusion: The Perfect Combination

**The orchestrator agent is the first pattern where I felt the perfect combination of observability, customizability, and agents at scale.** In this lesson, we spun up many, many agents with dedicated focus context effortlessly. We can of course clean up our agents with a single command. We can control it all and manage our compute better, faster than ever before.

**Any release or system that enables you to increase the information rate between your agents and your work requires your attention, requires your focus.** The orchestrator agent is one of those systems.

I'll see you in the next Agentic Horizon lesson.
