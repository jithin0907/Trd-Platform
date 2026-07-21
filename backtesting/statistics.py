class Statistics:
    """
    Calculates professional backtesting statistics.
    """

    @staticmethod
    def calculate(trades):

        total_trades = 0
        wins = 0
        losses = 0
        open_trades = 0

        gross_profit = 0.0
        gross_loss = 0.0

        total_rr = 0.0

        total_win_pips = 0.0
        total_loss_pips = 0.0

        longest_win_streak = 0
        longest_loss_streak = 0

        current_win_streak = 0
        current_loss_streak = 0

        # ===============================
        # Loop through all trades
        # ===============================

        for trade in trades:

            result = trade["result"]

            if result == "WIN":

                wins += 1
                total_trades += 1

                gross_profit += trade["profit_pips"]

                total_win_pips += trade["profit_pips"]

                total_rr += trade["rr"]

                current_win_streak += 1
                current_loss_streak = 0

                if current_win_streak > longest_win_streak:
                    longest_win_streak = current_win_streak

            elif result == "LOSS":

                losses += 1
                total_trades += 1

                gross_loss += abs(trade["profit_pips"])

                total_loss_pips += abs(trade["profit_pips"])

                total_rr += trade["rr"]

                current_loss_streak += 1
                current_win_streak = 0

                if current_loss_streak > longest_loss_streak:
                    longest_loss_streak = current_loss_streak

            else:

                open_trades += 1

        # ===============================
        # Calculations
        # ===============================

        if total_trades > 0:
            win_rate = (wins / total_trades) * 100
        else:
            win_rate = 0

        loss_rate = 100 - win_rate if total_trades > 0 else 0

        net_profit = gross_profit - gross_loss

        if gross_loss > 0:
            profit_factor = gross_profit / gross_loss
        else:
            profit_factor = 0

        if wins > 0:
            average_win = gross_profit / wins
        else:
            average_win = 0

        if losses > 0:
            average_loss = gross_loss / losses
        else:
            average_loss = 0

        if (wins + losses) > 0:
            average_rr = total_rr / (wins + losses)
        else:
            average_rr = 0

        return {

            "total_trades": total_trades,

            "wins": wins,

            "losses": losses,

            "open_trades": open_trades,

            "win_rate": round(win_rate, 2),

            "loss_rate": round(loss_rate, 2),

            "gross_profit": round(gross_profit, 2),

            "gross_loss": round(gross_loss, 2),

            "net_profit": round(net_profit, 2),

            "profit_factor": round(profit_factor, 2),

            "average_win": round(average_win, 2),

            "average_loss": round(average_loss, 2),

            "average_rr": round(average_rr, 2),

            "longest_win_streak": longest_win_streak,

            "longest_loss_streak": longest_loss_streak

        }