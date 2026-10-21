import { test, expect } from 'claude-code/testing'
import { lastBangCommand } from './register'

test('takes the last answer line that is a whole ! command', () => {
  expect(lastBangCommand('Check:\n\n`! ssh-add -l`\n')).toBe('! ssh-add -l')
  expect(lastBangCommand('Run:\n`! git status`\nThen send me the output.')).toBe('! git status')
  expect(lastBangCommand('`! git status`\nor\n`! git log -n 1`\nThat is all.')).toBe('! git log -n 1')
  expect(lastBangCommand('Run:\n```\n! npm test\n```')).toBe('! npm test')
  expect(lastBangCommand('Flow: an answer with `! cmd` → Enter\n\nAll good.')).toBeUndefined()
  expect(lastBangCommand('Use `!==` in JS')).toBeUndefined()
  expect(lastBangCommand('no commands here')).toBeUndefined()
})
