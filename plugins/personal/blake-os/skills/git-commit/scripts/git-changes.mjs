// Pre-bake the "what's changed" snapshot for git-commit.
// Always exits 0 — safe for non-repo or no-HEAD repos.
import { execFileSync } from "node:child_process";

const LINE_CAP = 200;

const safe = (args, fb) => {
	try {
		return execFileSync("git", args, {
			encoding: "utf-8",
			stdio: ["ignore", "pipe", "ignore"],
		}).trim();
	} catch {
		return fb;
	}
};

const emitCapped = (raw, emptyLabel) => {
	const lines = raw.split("\n");
	const trailingEmpty = lines.length > 0 && lines.at(-1) === "";
	const real = trailingEmpty ? lines.slice(0, -1) : lines;
	if (real.length === 0 || (real.length === 1 && real[0] === "")) {
		process.stdout.write(`${emptyLabel}\n`);
	} else if (real.length > LINE_CAP) {
		process.stdout.write(real.slice(0, LINE_CAP).join("\n"));
		process.stdout.write(`\n(... ${real.length - LINE_CAP} more files truncated ...)\n`);
	} else {
		process.stdout.write(`${real.join("\n")}\n`);
	}
};

const root = safe(["rev-parse", "--show-toplevel"], "");
process.stdout.write(`in_repo: ${root ? "yes" : "no"}\n`);
if (!root) process.exit(0);

process.stdout.write("---status---\n");
emitCapped(safe(["status", "--short"], ""), "(working tree clean)");

const hasHead = safe(["rev-parse", "--verify", "--quiet", "HEAD"], "") !== "";
process.stdout.write("---diffstat---\n");
if (!hasHead) {
	process.stdout.write("(no HEAD yet — initial commit; status above lists all files to be added)\n");
} else {
	emitCapped(safe(["diff", "HEAD", "--stat", "--ignore-submodules=all"], ""), "(no changes against HEAD)");
}
