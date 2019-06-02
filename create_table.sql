USE [Commodity_Spot_Rates]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING OFF
GO

CREATE TABLE [dbo].[invest_dot_com](
	[sys_id] [int] IDENTITY(1,1) NOT NULL,
	[commodity] [nvarchar](30) NOT NULL,
	[month] [nvarchar](6) NOT NULL,
	[last] [float] NOT NULL,
	[high] [float] NOT NULL,
	[low] [float] NOT NULL,
	[chg] [float] NOT NULL,
	[chg_pct] [float] NOT NULL,
	[time] [nvarchar](8) NOT NULL,
	[upload_date] [datetime] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[sys_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


