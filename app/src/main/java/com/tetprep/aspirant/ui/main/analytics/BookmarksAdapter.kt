package com.tetprep.aspirant.ui.main.analytics

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.tetprep.aspirant.data.local.entity.BookmarkEntity
import com.tetprep.aspirant.databinding.ItemBookmarkBinding

class BookmarksAdapter(
    private val onDeleteClick: (BookmarkEntity) -> Unit
) : ListAdapter<BookmarkEntity, BookmarksAdapter.BookmarkViewHolder>(DiffCallback) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): BookmarkViewHolder {
        val binding = ItemBookmarkBinding.inflate(
            LayoutInflater.from(parent.context), parent, false
        )
        return BookmarkViewHolder(binding, onDeleteClick)
    }

    override fun onBindViewHolder(holder: BookmarkViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class BookmarkViewHolder(
        private val binding: ItemBookmarkBinding,
        private val onDeleteClick: (BookmarkEntity) -> Unit
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(bookmark: BookmarkEntity) {
            binding.tvBookmarkTitle.text = bookmark.title
            binding.tvBookmarkSnippet.text = bookmark.snippet
            binding.btnDeleteBookmark.setOnClickListener {
                onDeleteClick(bookmark)
            }
        }
    }

    companion object DiffCallback : DiffUtil.ItemCallback<BookmarkEntity>() {
        override fun areItemsTheSame(oldItem: BookmarkEntity, newItem: BookmarkEntity): Boolean =
            oldItem.id == newItem.id

        override fun areContentsTheSame(oldItem: BookmarkEntity, newItem: BookmarkEntity): Boolean =
            oldItem == newItem
    }
}
