import type { Register } from 'claude-code'

// A command is a whole line of the answer: `! cmd`, or `! cmd` inside a code block; the last one wins.
// Mentions inside a sentence (diagrams, examples) do not count.
const WHOLE_LINE = /^[ \t]*`?(! [^`\n]+?)`?[ \t]*$/

export function lastBangCommand(answer: string): string | undefined {
  let cmd: string | undefined
  for (const line of answer.split('\n')) cmd = line.match(WHOLE_LINE)?.[1].trim() ?? cmd
  return cmd
}

export const register: Register = on => {
  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    if (e.agentId !== undefined || e.reason !== 'answer') return result

    const cmd = lastBangCommand(e.answer)
    if (!cmd) return result

    // Never overwrite what the person has already started typing
    const box = await $.prompt.read()
    if (box.text.trim() === '') await $.prompt.fill({ text: cmd, mode: 'replace' })

    return result
  })

  // prompt.fill does not switch the prompt box into bash mode: `! cmd` would go out as a plain prompt.
  // Intercept such a prompt, run the command here and hand its output to the model.
  on('prompt.submit', async ($, e, next) => {
    if (e.origin.kind !== 'composer' || e.command || !e.text.startsWith('! ')) return next(e)

    const cmd = e.text.slice(2).trim()
    const ran = await $.process
      .run(['/bin/zsh', '-lc', cmd], { timeoutMs: 600_000 })
      .catch(err => ({ exitCode: 1, stdout: '', stderr: String(err) }))

    // The model gets the output instead of `! cmd`, so it sees the result and keeps working
    const exit = ran.exitCode ? `\n<exit-code>${ran.exitCode}</exit-code>` : ''
    return next({
      ...e,
      text: `<bash-input>${cmd}</bash-input>\n<bash-stdout>${ran.stdout}</bash-stdout><bash-stderr>${ran.stderr}</bash-stderr>${exit}`,
    })
  }).catch(($, e, next) => (next.called ? next(e) : { drop: 'bang-prefill: could not run the command' }))
}
