# Claude Agent SDK: Building Custom Agents

## Introduction

Agentic engineering leads every engineer down one single path: **Better agents, more agents, and then custom agents**. If you can prompt engineer and context engineer a single agent successfully, then the next step is to add more agents. Scale your compute to scale your impact. Then once you learn to delegate work to sub agents and new primary agents, there's only one place left to go: **Custom agents**.

But why isn't Cloud Code, Codeex CLI, or the Gemini CLI enough? The out-of-the-box agents are incredible, but there's a massive problem with these tools. **They're built for everyone's codebase, not yours.** This mismatch can cost you hundreds of hours and millions of tokens scaling as your codebase grows.

This lesson is about flipping that equation. Here we master custom agents so your compute works for your domain, your problems, your edge cases. This is where all the alpha is in engineering. It's in the hard specific problems that most engineers and most agents can't solve out of the box.

In this advanced lesson, we showcase eight unique custom agents built on the Cloud Code SDK. Each one showing you how to deploy across your stack, products, and engineering life cycle. The agents are on the horizon. It's time to master agents by going all the way to the bare metal to the custom agent so you can scale your compute far beyond the rest.

In the building specialized agents codebase inside of apps, you can see eight custom agents. Let's start simple with the pong agent.

---

## Agent 1: The Pong Agent - Understanding System Prompts

### Demonstration

Here is a simple agent that's going to showcase the most important aspect of custom agents. You can see we have a simple, concise user prompt and agent response. And we have some session stats.

Let's run this again. All right, let's go ahead and change our prompt: "Hello." Simple prompt. We're just getting started with custom agents. I said hello. It just responded with "pong." Okay.

"Summarize this codebase." Okay, there's my user prompt. And once again, the pong agent is responding again with "pong." What's going on here? Let's ask it what's happening: "Can you do anything other than pong?" Okay, there's a user prompt and okay, so all this agent does is pong.

Type one more here. Just going to write "ping." This silly agent encapsulates the most important concept when you're building custom agents. **No matter what we prompt here, the response is always pong.** Why is that?

### The System Prompt: The Most Important Concept

Let's dive into this file. So the first most important concept is none other than **the system prompt**. We are using the Cloud Code SDK and we're setting up only two things. We're modifying just two aspects of this agent, but it changes everything.

So you can see `cloud_options` and here the system prompt. So let's open up the system prompt. You can see we have this dedicated `load_system_prompt` method. There's the path to the prompt. Let's open it.

We have completely overwritten the Claude Code system prompt with this title of our agent purpose. And we have a simple three-line instruction:

```text
You are a pong agent.
Always respond exactly with pong.
```

That's it. **The system prompt is the most important element of your custom agents with zero exceptions.** We are modifying the core for specifically the prompt.

But now we have two very important prompts to pay attention to:

- **System prompts** and **user prompts**

**The system prompt affects every single user prompt the agent runs. Every single one.** So all of your work is multiplied by your system prompt.

### How the Cloud Code SDK Works

So how does the Cloud Code SDK work? Let's go ahead and break down the key ideas. The SDK works like this:

1. You set up your options
2. You set up your agent
3. Here we're just running the query
4. Then you handle the response

The Cloud Code SDK is a powerful tool for putting together agents as you'll see as we progress. All the pieces are there and they're incrementally adoptable. And then lastly, we're just doing some logging. That's it. That's the end of our agent, right? A simple 150 line Pong agent. Most of this is just logging.

We're setting up the agent. We're then querying the agent. We're then handling the response of the agent. And take note of these specific blocks that you can report:

- We have our agent message blocks
- We have a result message
- And you can parse specific information out of these as you'll see as we progress

But this is the pong agent and this showcases the power of the system prompt. Remember all that work that the Claude Code team has put into making a great agent, right? **The Claude Code agent that you know and love is now gone.** Okay, you have to be very careful with the system prompt. **We now have a new product. This is not Claude Code anymore.** Okay, it might be using the same model, but the system prompt is truly what builds the agent.

Now, of course, we are still using the tools. That's important to call out here as you'll see as we progress into more and more capable custom agents.

---

## Agent 2: The Echo Agent - Custom Tools and Continuous Conversations

### Overview

Let's move on to our second agent, the echo agent. Inside of our echo agent, you can see a similar structure. We have a single Python script here that we're going to execute: `uv run echo_agent.py`. And we're going to see a similar structure, right?

Right, we have our Echo agent kicking off user prompt agent response. But here we have something different. Here we have of course a custom tool. So our agent is saying "I'll use this tool" and then we have this tool call block here. And then we have the response of the tool call and then our agent response.

All right. So these are all unique elements coming out of our agent. You want to be keeping track of these, right? **Keep track of the core four.** If you understand the core 4 and how each element flows and controls your agent, you will understand compute and you'll understand how to scale your compute.

### Using Custom Tools

Let's go ahead and echo ourselves. So, I'm going to say "echo this string and then I want it in reverse in uppercase. Repeat two times here." We're just playing with the tool that our custom agent has.

All right. So, there's the user prompt. There's that call in reverse. This text comes out to "custom agents are powerful." We ask it to repeat and go uppercase. So that's exactly what our agent has done.

Okay, we're scaling up a little more. We're adding a few more capabilities to our agent as we explore custom agents.

### Agent Structure

Let's understand what's going on here in the Echo agent. Same structure. I always love collapsing everything and you can just quickly understand what's going on. We have:

- `main`
- We have a tool
- And we have our system prompt

**Always look for the system prompt and then look for the custom tools.**

We have a couple parameters here. Then we have something special. So once again, you can always just search `cloud_code_options`. We have an MCP server built in this script: `create_sdk_mcp_server` and we're passing in a single tool. So this builds an entire MCP server in memory for our agent. **This is super powerful.**

### Building Custom Tools

So let's look at our echo tool and understand what it does. Tools for your Cloud Code SDK. They're built like this:

- A decorator
- We then have the name
- We have the description

So keep in mind **the description of your tool tells your agent how to use it** in addition to the actual parameters that get passed in to your tool and the actual arguments. You just pass in a dict and then you do whatever you want to do inside of your tool.

Here we step back into traditional deterministic code, right? It's a tool call. Do whatever you want, but be sure to respond in the proper format. You can see here, here's our log. Here's the transforms we were doing, right? Just a small example tool call for our agent. This is a custom agent with a custom tool set.

### Model Selection

Now something interesting here as well. You can see we are running Claude Haiku. We have downgraded our model to a cheaper less intelligent but much faster model. Right? This is a simple agent. It doesn't need powerful intelligence. So we've dropped down the model.

As we progress through each agent keep in mind we have the 12 leverage points of agent coding that we're paying attention to. But whenever you see `cloud_code_options` isolate the core four. How will the core 4 be managed given this setup?

### Continuous Conversations with SDK Client

Now, we have something else here that's important to call out. We're using the Claude SDK client class instead of our pong agent where we were just using that `query` command. All right, so **`query` is for one-off prompts and the Claude SDK client is for continuous conversations.**

Let me show you exactly what I mean here. Let's clear this and let's run this once again with follow-up. So, if we kick this off, our agent is going to run that same prompt like normal, but then it's going to continue the conversation. We're going to pass in another follow-up prompt. I'm going to say "concisely summarize our conversation in bullet points."

And so, here it is, right? Our agent quickly responds, follow-up response, concise summary. 1 2 3 4. Our agent has kept track of the conversation because we're using the Claude SDK client. And because we've written multiple query calls, you can see we have two here, follow-up prompt and the original user prompt.

All right, so we have both the tool use block that we care about and we have the text block. You can stream all the messages coming back out from your agent after you query and just take them in, right? Take them in, do whatever you want with them.

Here, of course, we're just logging with clean, rich panels, concisely communicating what's happening with our agent. **If you don't know what your agent is doing, if you don't adopt your agent's perspective, it will be hard to improve them and tweak them and manage them.** So, that's what we're doing here.

And you can see the follow-up prompt. We fired off that additional query and we just looked for that one response, right? We're looking for a tool use block. And really, we only were looking for the text block here, right? This is not actually that useful.

### Understanding Tool Context

This is a custom agent with a few more capabilities, right? We've specified the model. We've given it a custom tool to work with. But here's something interesting that if you're using these agents left and right, you probably haven't been paying attention to.

If we run this same agent and we just drop everything down here and we just say "list your available tools," we are actually still running a lot of the Claude Code baked in tool set. So check this out, right? These are all the Cloud Code tools plus our tool. And so everything that's going into your agent winds up in the context window at some point.

**We have 15 extra tools, 15 extra options that our agent has to choose from and select to do the job we've asked it.** Now, our Echo agent does not need any of these tools. All right? And so, as we progress, we're going to fine-tune. We're going to get more control over our agent.

If you ever run the `/context` command, understand what's going into your agent. You know that these 15 tools consumes context. It consumes space in your agent's mind. We're going to learn how to control that knob in our next agent.

### Echo System Prompt

The last thing we want to point out here is our Echo system prompt. Okay, very simple, right? Again, it's important to call out **this is not the Claude Code product anymore.** As soon as you touch the system prompt and once you start dialing into the tools, you change the product, you change the agent.

All right, so you can see here title purpose echo agent use the tool when asked. All right. So there's not a lot of happening here, but there is a lot that was happening that isn't happening anymore. Right? If that makes sense. We have blown away the Claude Code system prompt. We have completely overwritten it.

Now, it is important to mention you can append system prompt, right? You can just add on to what's already there. This is also powerful. This is more of a way to extend Cloud Code versus overwrite it and build a true custom agent.

All right, let's continue. Let's progress. Let's get more control over our agents. Let's scale this up and let's look at a new form factor for agents.

---

## Agent 3: The Micro SDLC Agent - Multi-Agent Orchestration

### Overview

Now we arrive at custom micro SDLC agent. Let's understand the structure of this codebase. Backend, frontend, reviews, specs and a couple of test files. So let's go ahead and just kick this off. We already have this running here. Backend, frontend. Let's see exactly what this is.

You probably understand what's going on here, right? **We have an agent-by-agent task board where we hand off work from one agent to another agent in a kind of micro software development life cycle.**

Now you can see here we have a couple tasks already shipped. We have some aired ones over here. Let's just go ahead create a new task. We're going to do something really stupid and simple. I just want to showcase the workflow and showcase the capabilities that you can build into your user interfaces with agents.

So, "update titles." This is just going to be super simple. Update the HTML title and header title to be "plan build review and ship agents." Okay. And now we have that here, right? Update titles. Then we just drag it into plan. And now this workflow is going to kick off.

### Multi-Agent System in Action

Let's go ahead and refocus on the actual agent running on the back end. So let's just collapse the frontend there and let's see what our agent is doing. **The difference here is we have a multi-agent system, right?** We're not just deploying a single agent anymore. We're deploying multiple agents inside of our UI.

So now we have a planner agent. It's noticing it's thinking, right? We have:

- Planner thinking
- Planner tool calls
- Hook interceptions, right? Tool allowed
- We have permission system inside of this

It has the full structure. And now it's going to start updating this code, right? It's a simple title change. This isn't, you know, rocket science, but we should see our title update here. And we should see our HTML title update as well, right? **It is operating on itself.**

### Real-Time Monitoring

Couple cool things, right? You can kind of build out your own multi-agent orchestration system however you want. We have:

- The messages on the left - so the total messages getting streamed to the frontend via websockets
- And then we have the total tool calls on the right

Okay. So our agent is working. You can see there the planning is incrementing. But you can see here our builder agent is now processing. And this is really cool, right? Our build agent is now processing. So the planner is done.

You know, you'll notice the UI is going to be a little kind of glitchy here because it is updating on itself. And so it's, you know, actively starting and restarting the server and the client. Um, but that's fine. Our websocket should pick this up and continue processing.

So there you can see the spec. You know, we're operating on that plan. We're operating in the review now. There we go. We can see that we're in the review step now.

### Workflow Execution

Okay. So very cool way to just kind of see how agents can work together and then you just package it in a nice UI. Then you can do more than you ever could before, frankly. Right. **We have a dedicated workflow working step by step by step: plan, build, review, and handing it off to the next stage in the process.**

Okay, you can see here our reviewer agent, there's all of its tools, and you can see it just operating, doing work for us, right? **We're using a lot of the out-of-the-box Cloud Code tools, right? If you don't need to reinvent the wheel, don't do it.** Let's be super clear about this. **The Cloud Code SDK running the base Cloud Code agent is incredible.** We've been using it since Cloud Code was released.

Uh, you can see here we just moved to shipped. There we go. Update titles. And you can see here, guess what happened? "Plan, build, review, and ship agents." Both titles updated. **This work shipped with a single prompt outside the loop.** Right? This is a perfect example of an outloop review system using the Peter framework. We dialed into this a ton inside of TAC. If you haven't finished the TAC lessons, you should probably stop watching this video immediately and finish TAC. It's all about transitioning from in-loop to outloop to eventually ZTE.

---

## Conclusion: Scaling Compute Through Custom Agents

The agent is compute scaled. You want to know how to deploy this across your tools, products, services for yourself, for your engineering work, and for your users and customers. And the Cloud Code SDK and other agent SDKs. These are all powerful toolkits you can use to control the core for within your agents to scale them intelligently.

**If you're doing one-size-fits-all work, use the out-of-the-box agent.** Don't think super hard about this. Just deploy compute to get the job done. But as your work becomes more specialized, as you deploy agents across all aspects of your engineering, you first want **better agents, more agents, and then custom agents.**

This is a codebase you're going to want to ultra think about and understand how you can extend and use the ideas we've discussed here. **Deploying effective compute and deploying effective agents is all about finding the constraints in your personal workflow and in your products.**

Think about repeat workflows that can benefit from an agent inside of:

- A script
- A data stream
- An interactive terminal
- All the way up to user interfaces

That can tackle high return on investment problems in your tools for your team and for your business.

**Agent coding is not so much about what we can do anymore. It's about what we can teach our agents to do.** This is how we push our compute to its useful limits. Follow this path to unlock massive value for your tools and products: **Better agents, more agents, and then custom agents.**

I'll see you in the next Agentic Horizon extended lesson.
