package com.trendscope.app

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.card.MaterialCardView
import com.trendscope.app.network.DomainFeeds

class CategoryAdapter(
    private val categories: List<String>,
    private val onClick: (String) -> Unit
) : RecyclerView.Adapter<CategoryAdapter.ViewHolder>() {

    private val colors = listOf(
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9",
        "#F0B27A", "#82E0AA", "#F1948A", "#85929E", "#73C6B6",
        "#E59866", "#7FB3D8", "#C39BD3", "#76D7C4", "#F8C471",
        "#7DCEA0", "#B2BABB", "#A3E4D7", "#FAD7A0"
    )

    inner class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val card: MaterialCardView = view.findViewById(R.id.cardCategory)
        val text: TextView = view.findViewById(R.id.tvCategoryName)
        val emoji: TextView = view.findViewById(R.id.tvCategoryEmoji)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_category, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val category = categories[position]
        val emoji = DomainFeeds.getCategoryEmoji(category)
        holder.emoji.text = emoji
        holder.text.text = category
        holder.card.setCardBackgroundColor(
            android.graphics.Color.parseColor(colors[position % colors.size])
        )
        holder.card.setOnClickListener { onClick(category) }
    }

    override fun getItemCount() = categories.size
}
