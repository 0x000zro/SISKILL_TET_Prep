package com.tetprep.aspirant.utils

import android.content.Context
import android.widget.TextView
import io.noties.markwon.Markwon
import io.noties.markwon.ext.strikethrough.StrikethroughPlugin
import io.noties.markwon.ext.tables.TablePlugin

class MarkdownRenderer(context: Context) {

    private val markwon: Markwon = Markwon.builder(context)
        .usePlugin(TablePlugin.create(context))
        .usePlugin(StrikethroughPlugin.create())
        .build()

    fun render(textView: TextView, markdownText: String) {
        markwon.setMarkdown(textView, markdownText)
    }

    companion object {
        @Volatile
        private var INSTANCE: MarkdownRenderer? = null

        fun getInstance(context: Context): MarkdownRenderer {
            return INSTANCE ?: synchronized(this) {
                val instance = MarkdownRenderer(context.applicationContext)
                INSTANCE = instance
                instance
            }
        }
    }
}
