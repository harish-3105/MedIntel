// Enhanced chat bubble with risk badges, citations, and TTS playback

import { motion } from 'framer-motion';

const riskColors = {
  Green: 'risk-badge-green',
  Amber: 'risk-badge-amber',
  Red: 'risk-badge-red',
};

// Simple markdown to HTML converter for basic formatting
const renderMarkdown = (text) => {
  if (!text) return '';
  
  let html = text
    // Bold: **text** or __text__
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/__(.+?)__/g, '<strong>$1</strong>')
    // Italic: *text* or _text_
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/_(.+?)_/g, '<em>$1</em>')
    // Line breaks
    .replace(/\n/g, '<br/>');
  
  return html;
};

function ChatBubble({ message, onPlayAudio, onStopAudio, showAudio, speaking }) {
  const isAssistant = message.role === 'assistant';
  const riskBadge = isAssistant && message.riskLevel ? riskColors[message.riskLevel] : null;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, translateY: 20 }}
      animate={{ opacity: 1, translateY: 0 }}
      transition={{ duration: 0.3 }}
      className={`glass-card p-5 ${
        isAssistant ? 'ml-0 mr-12' : 'ml-12 mr-0 border-primary/20 bg-primary/5'
      }`}
    >
      <div className="mb-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <p className="text-xs font-semibold uppercase tracking-wider text-white/60">
            {isAssistant ? '🩺 MedIntel' : '👤 You'}
          </p>
          {message.timestamp && (
            <span className="text-xs text-white/40">
              {new Date(message.timestamp).toLocaleTimeString()}
            </span>
          )}
        </div>
        {riskBadge && <span className={riskBadge}>{message.riskLevel}</span>}
      </div>

      {message.summary && (
        <p className="mb-2 text-sm font-semibold text-primary">{message.summary}</p>
      )}

      <div 
        className="prose prose-invert max-w-none text-base leading-relaxed text-white/90"
        dangerouslySetInnerHTML={{ __html: renderMarkdown(message.content) }}
      />

      {message.analysis && (
        <div className="mt-4 overflow-hidden rounded-xl border border-primary/30 bg-gradient-to-br from-primary/10 to-transparent">
          <div className="border-b border-primary/30 bg-primary/20 px-4 py-3">
            <h3 className="text-lg font-bold text-white">📋 Medical Analysis Report</h3>
          </div>
          
          {message.analysis.conditions && message.analysis.conditions.length > 0 && (
            <div className="border-b border-white/10 p-4">
              <h4 className="mb-3 text-sm font-semibold uppercase tracking-wider text-primary">
                Possible Conditions
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-white/10 text-left">
                      <th className="pb-2 pr-4 font-semibold text-white/70">#</th>
                      <th className="pb-2 pr-4 font-semibold text-white/70">Condition</th>
                      <th className="pb-2 pr-4 font-semibold text-white/70">Confidence</th>
                      <th className="pb-2 font-semibold text-white/70">Details</th>
                    </tr>
                  </thead>
                  <tbody>
                    {message.analysis.conditions.map((cond, idx) => (
                      <tr key={idx} className="border-b border-white/5">
                        <td className="py-3 pr-4 text-white/60">{idx + 1}</td>
                        <td className="py-3 pr-4 font-medium text-white">
                          {cond.name}
                          {cond.emergency && (
                            <span className="ml-2 text-xs text-red-400">⚠️ EMERGENCY</span>
                          )}
                        </td>
                        <td className="py-3 pr-4">
                          <span className="rounded-full bg-primary/20 px-2 py-1 text-xs text-primary">
                            {cond.confidence}
                          </span>
                        </td>
                        <td className="py-3 text-xs text-white/60">{cond.reasoning}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 border-b border-white/10 p-4">
            <div>
              <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-white/60">
                Severity Level
              </p>
              <p className={`text-lg font-bold ${
                message.analysis.severity === 'CRITICAL' ? 'text-red-400' :
                message.analysis.severity === 'HIGH' ? 'text-orange-400' :
                message.analysis.severity === 'MODERATE' ? 'text-yellow-400' :
                'text-green-400'
              }`}>
                {message.analysis.severity || 'N/A'}
              </p>
            </div>
            <div>
              <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-white/60">
                Urgency Level
              </p>
              <p className={`text-lg font-bold ${
                message.analysis.urgency === 'EMERGENCY' ? 'text-red-400' :
                message.analysis.urgency === 'URGENT' ? 'text-orange-400' :
                message.analysis.urgency === 'ROUTINE' ? 'text-yellow-400' :
                'text-green-400'
              }`}>
                {message.analysis.urgency || 'N/A'}
              </p>
            </div>
          </div>

          {message.analysis.red_flags && message.analysis.red_flags.length > 0 && (
            <div className="border-b border-white/10 bg-red-500/10 p-4">
              <h4 className="mb-2 text-sm font-semibold uppercase tracking-wider text-red-400">
                🚩 Red Flags Detected
              </h4>
              <ul className="space-y-1 text-sm text-white/80">
                {message.analysis.red_flags.map((flag, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-red-400">•</span>
                    <span>{flag}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {message.analysis.recommendations && message.analysis.recommendations.length > 0 && (
            <div className="p-4">
              <h4 className="mb-2 text-sm font-semibold uppercase tracking-wider text-primary">
                📌 Recommendations
              </h4>
              <ol className="space-y-2 text-sm text-white/80">
                {message.analysis.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="font-semibold text-primary">{idx + 1}.</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>
      )}

      {message.nextSteps && message.nextSteps.length > 0 && (
        <div className="mt-4 rounded-xl border border-primary/20 bg-primary/5 p-3">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-primary">
            Next Steps
          </p>
          <ul className="space-y-1.5 text-sm text-white/80">
            {message.nextSteps.map((step, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-primary">→</span>
                <span>{step}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {message.sources && message.sources.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {message.sources.map((source, idx) => (
            <span
              key={idx}
              className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-white/60"
            >
              📚 {source}
            </span>
          ))}
        </div>
      )}

      {message.confidence && (
        <div className="mt-2 flex items-center gap-3 text-xs text-white/40">
          <span>Confidence: {message.confidence}</span>
          {message.model_used && (
            <span className="text-teal-400/60">• {message.model_used.toUpperCase()}</span>
          )}
        </div>
      )}

      {showAudio && isAssistant && message.content && (
        <div className="mt-3 flex gap-2">
          {!speaking ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onPlayAudio(message.content)}
              className="flex items-center gap-2 rounded-xl border border-primary/30 bg-primary/10 px-4 py-2 text-sm text-primary transition-all hover:bg-primary/20"
            >
              <span>▶</span>
              <span>Play Audio</span>
            </motion.button>
          ) : (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onStopAudio}
              className="flex items-center gap-2 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-2 text-sm text-red-400 transition-all hover:bg-red-500/20"
            >
              <span>⏹</span>
              <span>Stop Audio</span>
            </motion.button>
          )}
        </div>
      )}
    </motion.div>
  );
}

export default ChatBubble;
